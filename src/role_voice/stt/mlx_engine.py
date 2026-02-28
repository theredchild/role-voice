from __future__ import annotations

import time

import numpy as np
from numpy.typing import NDArray

from role_voice.stt.base import STTEngine, TranscriptionResult


class MLXWhisperEngine(STTEngine):
    """STT engine using mlx-whisper (Apple Silicon optimized)."""

    def __init__(self, model_name: str = "mlx-community/whisper-turbo"):
        self._model_name = model_name
        self._loaded = False

    def load_model(self) -> None:
        import mlx_whisper

        # Warm up: transcribe silence to trigger model download + JIT compilation
        silence = np.zeros(16000, dtype=np.float32)
        mlx_whisper.transcribe(silence, path_or_hf_repo=self._model_name)
        self._loaded = True

    def transcribe(
        self,
        audio: NDArray[np.float32],
        sample_rate: int = 16000,
        language: str | None = "en",
    ) -> TranscriptionResult:
        import mlx_whisper

        t0 = time.perf_counter()
        result = mlx_whisper.transcribe(
            audio,
            path_or_hf_repo=self._model_name,
            language=language,
            condition_on_previous_text=False,
        )
        elapsed = time.perf_counter() - t0

        return TranscriptionResult(
            text=result["text"].strip(),
            language=result.get("language"),
            duration_seconds=len(audio) / sample_rate,
            processing_seconds=elapsed,
        )

    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def engine_name(self) -> str:
        return f"mlx-whisper ({self._model_name})"
