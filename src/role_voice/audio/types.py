from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class AudioChunk:
    """A single chunk of audio data from the microphone."""

    data: NDArray[np.float32]
    sample_rate: int
    channels: int = 1


@dataclass
class AudioBuffer:
    """Accumulates AudioChunks during a recording session."""

    sample_rate: int
    chunks: list[NDArray[np.float32]] = field(default_factory=list)

    def append(self, chunk: AudioChunk) -> None:
        self.chunks.append(chunk.data)

    def to_array(self) -> NDArray[np.float32]:
        """Concatenate all chunks into a single contiguous array."""
        if not self.chunks:
            return np.array([], dtype=np.float32)
        return np.concatenate(self.chunks, axis=0)

    def duration_seconds(self) -> float:
        total_samples = sum(c.shape[0] for c in self.chunks)
        return total_samples / self.sample_rate

    def clear(self) -> None:
        self.chunks.clear()
