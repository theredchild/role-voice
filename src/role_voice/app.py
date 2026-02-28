from __future__ import annotations

import threading

from role_voice.audio.capture import AudioCapture
from role_voice.audio.preprocessing import AudioPreprocessor
from role_voice.config import AppConfig
from role_voice.input.hotkey import HotkeyListener
from role_voice.input.types import HotkeyEvent
from role_voice.stt.factory import create_stt_engine
from role_voice.targets.factory import create_target_dispatcher
from role_voice.ui.console import ConsoleUI


class RoleVoiceApp:
    """Main application orchestrator. Wires all modules together."""

    def __init__(self, config: AppConfig):
        self._config = config
        self._audio = AudioCapture(
            sample_rate=config.audio.sample_rate,
            channels=config.audio.channels,
            block_size=config.audio.block_size,
            device=config.audio.device,
        )
        self._preprocessor = (
            AudioPreprocessor(
                vad_threshold=config.vad.threshold,
                min_speech_duration_ms=config.vad.min_speech_duration_ms,
                min_silence_duration_ms=config.vad.min_silence_duration_ms,
            )
            if config.vad.enabled
            else None
        )
        self._stt = create_stt_engine(config.stt)
        self._target = create_target_dispatcher(config.target)
        self._hotkey = HotkeyListener(
            hotkey_str=config.hotkey.push_to_talk,
            callback=self._on_hotkey_event,
        )
        self._ui = ConsoleUI(
            show_transcription=config.ui.show_transcription,
            show_timing=config.ui.show_timing,
        )
        self._processing_lock = threading.Lock()

    def run(self) -> None:
        """Start the application. Blocks until interrupted."""
        self._ui.show_loading("Loading STT model...")
        self._stt.load_model()

        self._ui.show_ready(
            hotkey=self._config.hotkey.push_to_talk,
            target=self._target.target_name,
            engine=self._stt.engine_name,
        )

        self._hotkey.start()
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self) -> None:
        """Clean up all resources."""
        self._hotkey.stop()
        if self._audio.is_recording:
            self._audio.stop()

    def _on_hotkey_event(self, event: HotkeyEvent) -> None:
        if event == HotkeyEvent.PRESSED:
            self._ui.show_recording()
            self._audio.start()
        elif event == HotkeyEvent.RELEASED:
            buffer = self._audio.stop()
            threading.Thread(
                target=self._process_recording,
                args=(buffer,),
                daemon=True,
            ).start()

    def _process_recording(self, buffer: object) -> None:
        with self._processing_lock:
            audio = buffer.to_array()
            if len(audio) == 0:
                self._ui.show_empty_recording()
                return

            self._ui.show_processing()

            if self._preprocessor:
                audio = self._preprocessor.process(audio, self._config.audio.sample_rate)
                if len(audio) == 0:
                    self._ui.show_empty_recording()
                    return

            try:
                result = self._stt.transcribe(
                    audio,
                    sample_rate=16000,
                    language=self._config.stt.language,
                )
            except Exception as e:
                self._ui.show_error(f"Transcription failed: {e}")
                return

            if not result.text.strip():
                self._ui.show_empty_recording()
                return

            self._ui.show_result(result)

            try:
                self._target.dispatch(result.text)
            except Exception as e:
                self._ui.show_error(f"Dispatch failed: {e}")
