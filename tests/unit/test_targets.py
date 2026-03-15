from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from role_voice.targets.base import TargetDispatcher


class TestTargetDispatcher:
    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError):
            TargetDispatcher()


class TestClipboardDispatcher:
    @patch("role_voice.targets.clipboard.subprocess")
    @patch("role_voice.targets.clipboard.platform")
    def test_dispatch_macos(self, mock_platform: MagicMock, mock_subprocess: MagicMock) -> None:
        mock_platform.system.return_value = "Darwin"
        from role_voice.targets.clipboard import ClipboardDispatcher

        dispatcher = ClipboardDispatcher()
        dispatcher.dispatch("hello world")
        mock_subprocess.run.assert_called_once_with(["pbcopy"], input=b"hello world", check=True)


class TestTerminalDispatcher:
    @patch("role_voice.targets.terminal.subprocess")
    @patch("role_voice.targets.terminal.platform")
    def test_dispatch_macos(self, mock_platform: MagicMock, mock_subprocess: MagicMock) -> None:
        mock_platform.system.return_value = "Darwin"
        from role_voice.targets.terminal import TerminalDispatcher

        dispatcher = TerminalDispatcher(auto_execute=False)
        dispatcher.dispatch("test command")
        assert mock_subprocess.run.call_count == 2  # pbcopy + osascript

    @patch("role_voice.targets.terminal.subprocess")
    @patch("role_voice.targets.terminal.platform")
    def test_dispatch_linux(self, mock_platform: MagicMock, mock_subprocess: MagicMock) -> None:
        mock_platform.system.return_value = "Linux"
        from role_voice.targets.terminal import TerminalDispatcher

        dispatcher = TerminalDispatcher(auto_execute=False)
        dispatcher.dispatch("test command")
        mock_subprocess.run.assert_called_once_with(["xdotool", "type", "--delay", "0", "test command"], check=True)


class TestClaudeCodeDispatcher:
    @patch("role_voice.targets.claude_code.shutil")
    def test_raises_if_claude_not_found(self, mock_shutil: MagicMock) -> None:
        mock_shutil.which.return_value = None
        from role_voice.targets.claude_code import ClaudeCodeDispatcher

        with pytest.raises(RuntimeError, match="Claude Code CLI not found"):
            ClaudeCodeDispatcher()


class TestTargetFactory:
    def test_clipboard_target(self, default_config) -> None:
        from role_voice.targets.factory import create_target_dispatcher

        dispatcher = create_target_dispatcher(default_config.target)
        assert dispatcher.target_name == "clipboard"

    def test_invalid_target(self, default_config) -> None:
        from role_voice.targets.factory import create_target_dispatcher

        default_config.target.type = "nonexistent"
        with pytest.raises(ValueError, match="Unknown target type"):
            create_target_dispatcher(default_config.target)
