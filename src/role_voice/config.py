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


LOCAL_CONFIG_PATH = Path("config.yaml")
USER_CONFIG_PATH = Path.home() / ".config" / "role-voice" / "config.yaml"


def load_config(path: Path | None = None) -> tuple[AppConfig, Path | None]:
    """Load config from YAML file.

    Search order:
    1. Explicit path (if provided)
    2. ./config.yaml (project directory)
    3. ~/.config/role-voice/config.yaml (user global)
    4. Built-in defaults

    Returns:
        Tuple of (config, path_used) where path_used is None if using defaults.
    """
    if path is not None:
        if path.exists():
            with open(path) as f:
                data = yaml.safe_load(f) or {}
            return AppConfig(**data), path
        return AppConfig(), None

    # Check project directory first
    if LOCAL_CONFIG_PATH.exists():
        with open(LOCAL_CONFIG_PATH) as f:
            data = yaml.safe_load(f) or {}
        return AppConfig(**data), LOCAL_CONFIG_PATH

    # Then user global config
    if USER_CONFIG_PATH.exists():
        with open(USER_CONFIG_PATH) as f:
            data = yaml.safe_load(f) or {}
        return AppConfig(**data), USER_CONFIG_PATH

    # Fall back to defaults
    return AppConfig(), None
