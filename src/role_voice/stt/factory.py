from __future__ import annotations

import platform

from role_voice.config import STTConfig
from role_voice.stt.base import STTEngine


def create_stt_engine(config: STTConfig) -> STTEngine:
    """Create the appropriate STT engine based on config and platform."""
    engine_type = config.engine

    if engine_type == "auto":
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            engine_type = "mlx"
        else:
            engine_type = "faster-whisper"

    if engine_type == "mlx":
        from role_voice.stt.mlx_engine import MLXWhisperEngine

        return MLXWhisperEngine(model_name=config.model)
    elif engine_type == "faster-whisper":
        from role_voice.stt.faster_whisper_engine import FasterWhisperEngine

        return FasterWhisperEngine(
            model_size=config.model,
            device=config.device,
            compute_type=config.compute_type,
        )
    else:
        raise ValueError(f"Unknown STT engine: {engine_type}")
