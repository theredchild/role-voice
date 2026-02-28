from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class TranscriptionResult:
    """Result from an STT transcription."""

    text: str
    language: str | None = None
    duration_seconds: float = 0.0
    processing_seconds: float = 0.0


class STTEngine(ABC):
    """Abstract base class for speech-to-text engines."""

    @abstractmethod
    def load_model(self) -> None:
        """Pre-load the model into memory. Called once at startup."""
        ...

    @abstractmethod
    def transcribe(
        self,
        audio: NDArray[np.float32],
        sample_rate: int = 16000,
        language: str | None = "en",
    ) -> TranscriptionResult:
        """Transcribe an audio array to text."""
        ...

    @abstractmethod
    def is_loaded(self) -> bool:
        """Whether the model is loaded and ready."""
        ...

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Human-readable name of this engine."""
        ...
