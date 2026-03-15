#!/usr/bin/env python3
"""Quick microphone diagnostic tool.

Records 3 seconds of audio, shows the waveform stats, and optionally plays it back.
Usage: python scripts/test_microphone.py [--playback]
"""

from __future__ import annotations

import sys

import numpy as np
import sounddevice as sd


def main() -> None:
    playback = "--playback" in sys.argv
    sample_rate = 16000
    duration = 3

    print(f"Recording {duration}s of audio at {sample_rate}Hz...")
    print("Speak now!")

    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()

    audio = audio[:, 0]
    peak = np.max(np.abs(audio))
    rms = np.sqrt(np.mean(audio**2))

    print("\nResults:")
    print(f"  Samples: {len(audio)}")
    print(f"  Duration: {len(audio) / sample_rate:.1f}s")
    print(f"  Peak amplitude: {peak:.4f}")
    print(f"  RMS level: {rms:.4f}")
    print(f"  Signal detected: {'Yes' if peak > 0.01 else 'No (check microphone)'}")

    if playback:
        print("\nPlaying back...")
        sd.play(audio, samplerate=sample_rate)
        sd.wait()
        print("Done.")


if __name__ == "__main__":
    main()
