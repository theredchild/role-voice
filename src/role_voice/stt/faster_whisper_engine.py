from __future__ import annotations

import time

import numpy as np
from numpy.typing import NDArray

from role_voice.stt.base import STTEngine, TranscriptionResult


class FasterWhisperEngine(STTEngine):
    """STT engine using faster-whisper (CTranslate2 backend)."""

    def __init__(
        self,
        model_size: str = "base.en",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self._model_size = model_size
        self._device = device
        self._compute_type = compute_type
        self._model = None

    def load_model(self) -> None:
        from faster_whisper import WhisperModel

        self._model = WhisperModel(
            self._model_size,
            device=self._device,
            compute_type=self._compute_type,
        )

    def transcribe(
        self,
        audio: NDArray[np.float32],
        sample_rate: int = 16000,
        language: str | None = "en",
    ) -> TranscriptionResult:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        t0 = time.perf_counter()
        segments, info = self._model.transcribe(
            audio,
            language=language,
            beam_size=1,
            vad_filter=False,
        )
        text = " ".join(segment.text.strip() for segment in segments)
        elapsed = time.perf_counter() - t0

        return TranscriptionResult(
            text=text,
            language=info.language,
            duration_seconds=len(audio) / sample_rate,
            processing_seconds=elapsed,
        )

    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def engine_name(self) -> str:
        return f"faster-whisper ({self._model_size})"
