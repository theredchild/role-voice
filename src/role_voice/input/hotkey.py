from __future__ import annotations

import threading
from collections.abc import Callable

from pynput import keyboard

from role_voice.input.types import HotkeyEvent


class HotkeyListener:
    """Listens for a configurable push-to-talk hotkey.

    Fires PRESSED when the hotkey combination is held down
    and RELEASED when any key in the combination is let go.
    """

    def __init__(
        self,
        hotkey_str: str,
        callback: Callable[[HotkeyEvent], None],
    ):
        self._hotkey_str = hotkey_str
        self._callback = callback
        self._listener: keyboard.Listener | None = None
        self._hotkey_keys = keyboard.HotKey.parse(hotkey_str)
        self._pressed_keys: set = set()
        self._is_active = False
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start listening for the hotkey."""
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self) -> None:
        """Stop the hotkey listener."""
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key is None:
            return
        canonical = self._listener.canonical(key) if self._listener else key
        with self._lock:
            self._pressed_keys.add(canonical)
            if not self._is_active and self._all_hotkey_keys_pressed():
                self._is_active = True
                self._callback(HotkeyEvent.PRESSED)

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key is None:
            return
        canonical = self._listener.canonical(key) if self._listener else key
        with self._lock:
            self._pressed_keys.discard(canonical)
            if self._is_active and not self._all_hotkey_keys_pressed():
                self._is_active = False
                self._callback(HotkeyEvent.RELEASED)

    def _all_hotkey_keys_pressed(self) -> bool:
        return all(k in self._pressed_keys for k in self._hotkey_keys)

    @property
    def hotkey_str(self) -> str:
        return self._hotkey_str
