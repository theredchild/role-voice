from __future__ import annotations

from role_voice.config import TargetConfig
from role_voice.targets.base import TargetDispatcher


def create_target_dispatcher(config: TargetConfig) -> TargetDispatcher:
    """Create the appropriate target dispatcher based on config."""
    if config.type == "clipboard":
        from role_voice.targets.clipboard import ClipboardDispatcher

        return ClipboardDispatcher()
    elif config.type == "claude-code":
        from role_voice.targets.claude_code import ClaudeCodeDispatcher

        return ClaudeCodeDispatcher(extra_args=config.claude_args)
    elif config.type == "terminal":
        from role_voice.targets.terminal import TerminalDispatcher

        return TerminalDispatcher(auto_execute=config.auto_execute)
    else:
        raise ValueError(f"Unknown target type: {config.type}")
