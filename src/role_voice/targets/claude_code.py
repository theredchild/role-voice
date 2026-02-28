from __future__ import annotations

import shutil
import subprocess

from role_voice.targets.base import TargetDispatcher


class ClaudeCodeDispatcher(TargetDispatcher):
    """Sends transcribed text to Claude Code in print mode."""

    def __init__(self, extra_args: list[str] | None = None):
        self._extra_args = extra_args or []
        self._claude_path = shutil.which("claude")
        if not self._claude_path:
            raise RuntimeError(
                "Claude Code CLI not found in PATH. "
                "Install it from https://claude.ai/code"
            )

    def dispatch(self, text: str) -> None:
        cmd = [self._claude_path, "-p", *self._extra_args, text]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0 and result.stderr:
            print(f"Claude Code error: {result.stderr}")

    @property
    def target_name(self) -> str:
        return "claude-code"
