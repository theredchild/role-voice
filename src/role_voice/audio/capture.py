from __future__ import annotations

import threading

import numpy as np
import sounddevice as sd

from role_voice.audio.types import AudioBuffer, AudioChunk


class AudioCapture:
    """Manages microphone recording via sounddevice callback stream."""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        block_size: int = 1024,
        device: int | str | None = None,
    ):
        self._sample_rate = sample_rate
        self._channels = channels
        self._block_size = block_size
        self._device = device
        self._buffer = AudioBuffer(sample_rate=sample_rate)
        self._stream: sd.InputStream | None = None
        self._recording = threading.Event()

    def start(self) -> None:
        """Begin capturing audio from the microphone."""
        self._buffer.clear()
        self._recording.set()
        self._stream = sd.InputStream(
            samplerate=self._sample_rate,
            channels=self._channels,
            blocksize=self._block_size,
            dtype="float32",
            device=self._device,
            callback=self._audio_callback,
        )
        self._stream.start()

    def stop(self) -> AudioBuffer:
        """Stop recording and return the accumulated buffer."""
        self._recording.clear()
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        return self._buffer

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: object,
        status: sd.CallbackFlags,
    ) -> None:
        if self._recording.is_set():
            chunk = AudioChunk(
                data=indata[:, 0].copy(),
                sample_rate=self._sample_rate,
            )
            self._buffer.append(chunk)

    @property
    def is_recording(self) -> bool:
        return self._recording.is_set()
