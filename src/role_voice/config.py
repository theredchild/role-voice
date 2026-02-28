from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class AudioConfig(BaseModel):
    sample_rate: int = 16000
    channels: int = 1
    block_size: int = 1024
    device: int | str | None = None


class VADConfig(BaseModel):
    enabled: bool = True
    threshold: float = 0.5
    min_speech_duration_ms: int = 250
    min_silence_duration_ms: int = 100


class STTConfig(BaseModel):
    engine: str = "auto"
    model: str = "mlx-community/whisper-turbo"
    language: str | None = "en"
    device: str = "cpu"
    compute_type: str = "int8"


class HotkeyConfig(BaseModel):
    push_to_talk: str = "<ctrl>+<shift>"


class TargetConfig(BaseModel):
    type: str = "clipboard"
    auto_execute: bool = False
    claude_args: list[str] = Field(default_factory=list)


class UIConfig(BaseModel):
    show_transcription: bool = True
    show_timing: bool = True


class AppConfig(BaseModel):
    audio: AudioConfig = Field(default_factory=AudioConfig)
    vad: VADConfig = Field(default_factory=VADConfig)
    stt: STTConfig = Field(default_factory=STTConfig)
    hotkey: HotkeyConfig = Field(default_factory=HotkeyConfig)
    target: TargetConfig = Field(default_factory=TargetConfig)
    ui: UIConfig = Field(default_factory=UIConfig)


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "role-voice" / "config.yaml"


def load_config(path: Path | None = None) -> AppConfig:
    """Load config from YAML file, falling back to defaults."""
    if path is None:
        path = DEFAULT_CONFIG_PATH
    if path.exists():
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return AppConfig(**data)
    return AppConfig()
