from __future__ import annotations

from abc import ABC, abstractmethod


class TargetDispatcher(ABC):
    """Abstract base for dispatching transcribed text to a target."""

    @abstractmethod
    def dispatch(self, text: str) -> None:
        """Send the transcribed text to the target."""
        ...

    @property
    @abstractmethod
    def target_name(self) -> str:
        """Human-readable name of this target."""
        ...
