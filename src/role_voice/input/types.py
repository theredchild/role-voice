from __future__ import annotations

from enum import Enum, auto


class HotkeyEvent(Enum):
    PRESSED = auto()
    RELEASED = auto()
