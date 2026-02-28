from __future__ import annotations

from pathlib import Path

from role_voice.config import AppConfig, load_config


class TestAppConfig:
    def test_default_config(self) -> None:
        config = AppConfig()
        assert config.audio.sample_rate == 16000
        assert config.audio.channels == 1
        assert config.stt.engine == "auto"
        assert config.hotkey.push_to_talk == "<ctrl>+<shift>"
        assert config.target.type == "clipboard"

    def test_custom_values(self) -> None:
        config = AppConfig(
            audio={"sample_rate": 48000},
            stt={"engine": "mlx", "model": "custom-model"},
            target={"type": "terminal", "auto_execute": True},
        )
        assert config.audio.sample_rate == 48000
        assert config.stt.engine == "mlx"
        assert config.stt.model == "custom-model"
        assert config.target.type == "terminal"
        assert config.target.auto_execute is True


class TestLoadConfig:
    def test_load_from_file(self, tmp_config_file: Path) -> None:
        config = load_config(tmp_config_file)
        assert config.audio.sample_rate == 16000
        assert config.target.type == "clipboard"

    def test_load_nonexistent_returns_defaults(self, tmp_path: Path) -> None:
        config = load_config(tmp_path / "nonexistent.yaml")
        assert config == AppConfig()
