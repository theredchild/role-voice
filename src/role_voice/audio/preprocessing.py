from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class AudioPreprocessor:
    """Trims silence and normalizes audio using Silero VAD."""

    def __init__(
        self,
        vad_threshold: float = 0.5,
        min_speech_duration_ms: int = 250,
        min_silence_duration_ms: int = 100,
    ):
        self._vad_threshold = vad_threshold
        self._min_speech_ms = min_speech_duration_ms
        self._min_silence_ms = min_silence_duration_ms
        self._vad_model = None

    def _ensure_vad_loaded(self) -> None:
        if self._vad_model is None:
            from silero_vad import load_silero_vad

            self._vad_model = load_silero_vad()

    def process(self, audio: NDArray[np.float32], sample_rate: int) -> NDArray[np.float32]:
        """Trim silence, normalize, resample to 16kHz if needed."""
        audio = self._resample_if_needed(audio, sample_rate, target_rate=16000)
        audio = self._trim_silence(audio, sample_rate=16000)
        audio = self._normalize(audio)
        return audio

    def _trim_silence(self, audio: NDArray[np.float32], sample_rate: int) -> NDArray[np.float32]:
        """Use Silero VAD to find speech segments and trim silence."""
        self._ensure_vad_loaded()
        import torch
        from silero_vad import get_speech_timestamps

        wav_tensor = torch.from_numpy(audio)
        timestamps = get_speech_timestamps(
            wav_tensor,
            self._vad_model,
            threshold=self._vad_threshold,
            min_speech_duration_ms=self._min_speech_ms,
            min_silence_duration_ms=self._min_silence_ms,
            sampling_rate=sample_rate,
        )
        if not timestamps:
            return audio
        start = timestamps[0]["start"]
        end = timestamps[-1]["end"]
        return audio[start:end]

    @staticmethod
    def _normalize(audio: NDArray[np.float32]) -> NDArray[np.float32]:
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak
        return audio

    @staticmethod
    def _resample_if_needed(
        audio: NDArray[np.float32],
        source_rate: int,
        target_rate: int,
    ) -> NDArray[np.float32]:
        if source_rate == target_rate:
            return audio
        import soxr

        return soxr.resample(audio, source_rate, target_rate)
