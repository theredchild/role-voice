from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

from role_voice.config import AppConfig
from role_voice.stt.base import STTEngine, TranscriptionResult


@pytest.fixture
def sample_audio_16k() -> np.ndarray:
    """5 seconds of random audio at 16kHz (simulates speech)."""
    rng = np.random.default_rng(42)
    return rng.standard_normal(5 * 16000).astype(np.float32) * 0.5


@pytest.fixture
def silence_audio() -> np.ndarray:
    """1 second of silence at 16kHz."""
    return np.zeros(16000, dtype=np.float32)


class MockSTTEngine(STTEngine):
    """Mock STT engine for testing."""

    def __init__(self, response_text: str = "hello world"):
        self._response_text = response_text
        self._loaded = False

    def load_model(self) -> None:
        self._loaded = True

    def transcribe(
        self,
        audio: np.ndarray,
        sample_rate: int = 16000,
        language: str | None = "en",
    ) -> TranscriptionResult:
        return TranscriptionResult(
            text=self._response_text,
            language=language,
            duration_seconds=len(audio) / sample_rate,
            processing_seconds=0.01,
        )

    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def engine_name(self) -> str:
        return "mock-engine"


@pytest.fixture
def mock_stt_engine() -> MockSTTEngine:
    return MockSTTEngine()


@pytest.fixture
def default_config() -> AppConfig:
    return AppConfig()


@pytest.fixture
def tmp_config_file(tmp_path: Path) -> Path:
    config_content = """
audio:
  sample_rate: 16000
  channels: 1
stt:
  engine: auto
  language: en
hotkey:
  push_to_talk: "<ctrl>+<shift>"
target:
  type: clipboard
"""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_content)
    return config_path
