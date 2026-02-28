from __future__ import annotations

import platform
import subprocess

from role_voice.targets.base import TargetDispatcher


class ClipboardDispatcher(TargetDispatcher):
    """Copies transcribed text to the system clipboard."""

    def dispatch(self, text: str) -> None:
        if platform.system() == "Darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        else:
            # Linux: try xclip, fall back to xsel
            try:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode("utf-8"),
                    check=True,
                )
            except FileNotFoundError:
                subprocess.run(
                    ["xsel", "--clipboard", "--input"],
                    input=text.encode("utf-8"),
                    check=True,
                )

    @property
    def target_name(self) -> str:
        return "clipboard"
