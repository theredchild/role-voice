#!/usr/bin/env python3
"""Benchmark STT engine latency with various audio durations."""

from __future__ import annotations

import time

import numpy as np

from role_voice.config import AppConfig
from role_voice.stt.factory import create_stt_engine


def main() -> None:
    config = AppConfig()
    engine = create_stt_engine(config.stt)

    print(f"Engine: {engine.engine_name}")
    print("Loading model...")
    t0 = time.perf_counter()
    engine.load_model()
    print(f"Model loaded in {time.perf_counter() - t0:.2f}s\n")

    durations = [1.0, 3.0, 5.0, 10.0]
    print(f"{'Duration':>10} {'STT Time':>10} {'RTF':>8}")
    print("-" * 32)

    for dur in durations:
        samples = int(dur * 16000)
        audio = np.random.randn(samples).astype(np.float32) * 0.01
        result = engine.transcribe(audio, sample_rate=16000)
        rtf = result.processing_seconds / dur
        print(f"{dur:>8.1f}s {result.processing_seconds:>9.2f}s {rtf:>7.2f}x")


if __name__ == "__main__":
    main()
