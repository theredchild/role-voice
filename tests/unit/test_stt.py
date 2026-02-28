from __future__ import annotations

import numpy as np
import pytest

from role_voice.stt.base import STTEngine, TranscriptionResult


class TestTranscriptionResult:
    def test_creation(self) -> None:
        result = TranscriptionResult(
            text="hello world",
            language="en",
            duration_seconds=1.0,
            processing_seconds=0.5,
        )
        assert result.text == "hello world"
        assert result.language == "en"
        assert result.duration_seconds == 1.0
        assert result.processing_seconds == 0.5

    def test_defaults(self) -> None:
        result = TranscriptionResult(text="test")
        assert result.language is None
        assert result.duration_seconds == 0.0
        assert result.processing_seconds == 0.0


class TestSTTEngine:
    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError):
            STTEngine()


class TestMockEngine:
    def test_mock_engine_lifecycle(self, mock_stt_engine) -> None:
        assert not mock_stt_engine.is_loaded()
        mock_stt_engine.load_model()
        assert mock_stt_engine.is_loaded()

    def test_mock_engine_transcribe(self, mock_stt_engine) -> None:
        audio = np.zeros(16000, dtype=np.float32)
        result = mock_stt_engine.transcribe(audio)
        assert result.text == "hello world"
        assert result.duration_seconds == 1.0


class TestSTTFactory:
    def test_factory_auto_selection(self, default_config) -> None:
        from role_voice.stt.factory import create_stt_engine

        engine = create_stt_engine(default_config.stt)
        # On any platform, auto should return a valid engine
        assert engine.engine_name is not None

    def test_factory_invalid_engine(self, default_config) -> None:
        from role_voice.stt.factory import create_stt_engine

        default_config.stt.engine = "nonexistent"
        with pytest.raises(ValueError, match="Unknown STT engine"):
            create_stt_engine(default_config.stt)
