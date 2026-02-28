from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from role_voice.audio.types import AudioBuffer, AudioChunk


class TestAudioChunk:
    def test_creation(self) -> None:
        data = np.zeros(1024, dtype=np.float32)
        chunk = AudioChunk(data=data, sample_rate=16000)
        assert chunk.sample_rate == 16000
        assert chunk.channels == 1
        assert len(chunk.data) == 1024


class TestAudioBuffer:
    def test_empty_buffer(self) -> None:
        buf = AudioBuffer(sample_rate=16000)
        arr = buf.to_array()
        assert len(arr) == 0
        assert buf.duration_seconds() == 0.0

    def test_append_and_concatenate(self) -> None:
        buf = AudioBuffer(sample_rate=16000)
        chunk1 = AudioChunk(data=np.ones(1024, dtype=np.float32), sample_rate=16000)
        chunk2 = AudioChunk(data=np.ones(1024, dtype=np.float32) * 2, sample_rate=16000)
        buf.append(chunk1)
        buf.append(chunk2)

        arr = buf.to_array()
        assert len(arr) == 2048
        assert arr[0] == 1.0
        assert arr[1024] == 2.0

    def test_duration(self) -> None:
        buf = AudioBuffer(sample_rate=16000)
        chunk = AudioChunk(data=np.zeros(16000, dtype=np.float32), sample_rate=16000)
        buf.append(chunk)
        assert buf.duration_seconds() == 1.0

    def test_clear(self) -> None:
        buf = AudioBuffer(sample_rate=16000)
        chunk = AudioChunk(data=np.zeros(1024, dtype=np.float32), sample_rate=16000)
        buf.append(chunk)
        buf.clear()
        assert len(buf.to_array()) == 0


class TestAudioCapture:
    @patch("role_voice.audio.capture.sd")
    def test_start_creates_stream(self, mock_sd: MagicMock) -> None:
        from role_voice.audio.capture import AudioCapture

        capture = AudioCapture(sample_rate=16000)
        capture.start()
        assert capture.is_recording
        mock_sd.InputStream.assert_called_once()

    @patch("role_voice.audio.capture.sd")
    def test_stop_returns_buffer(self, mock_sd: MagicMock) -> None:
        from role_voice.audio.capture import AudioCapture

        capture = AudioCapture(sample_rate=16000)
        capture.start()
        buffer = capture.stop()
        assert not capture.is_recording
        assert buffer is not None
