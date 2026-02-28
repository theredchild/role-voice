from __future__ import annotations

import platform
import subprocess

from role_voice.targets.base import TargetDispatcher


class TerminalDispatcher(TargetDispatcher):
    """Types text into the currently focused terminal window.

    On macOS, uses pbcopy + Cmd+V via osascript (requires Accessibility permission).
    On Linux, uses xdotool for typing.
    """

    def __init__(self, auto_execute: bool = False):
        self._auto_execute = auto_execute

    def dispatch(self, text: str) -> None:
        if platform.system() == "Darwin":
            self._dispatch_macos(text)
        else:
            self._dispatch_linux(text)

    def _dispatch_macos(self, text: str) -> None:
        subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        script = 'tell application "System Events" to keystroke "v" using command down'
        if self._auto_execute:
            script += '\ntell application "System Events" to keystroke return'
        subprocess.run(["osascript", "-e", script], check=True)

    def _dispatch_linux(self, text: str) -> None:
        subprocess.run(["xdotool", "type", "--delay", "0", text], check=True)
        if self._auto_execute:
            subprocess.run(["xdotool", "key", "Return"], check=True)

    @property
    def target_name(self) -> str:
        return "terminal"
