from __future__ import annotations

from unittest.mock import MagicMock, patch

from role_voice.input.types import HotkeyEvent


class TestHotkeyEvent:
    def test_enum_values(self) -> None:
        assert HotkeyEvent.PRESSED.name == "PRESSED"
        assert HotkeyEvent.RELEASED.name == "RELEASED"


class TestHotkeyListener:
    @patch("role_voice.input.hotkey.keyboard")
    def test_start_creates_listener(self, mock_kb: MagicMock) -> None:
        from role_voice.input.hotkey import HotkeyListener

        mock_kb.HotKey.parse.return_value = [mock_kb.Key.ctrl, mock_kb.Key.shift]
        callback = MagicMock()
        listener = HotkeyListener("<ctrl>+<shift>", callback)
        listener.start()
        mock_kb.Listener.assert_called_once()

    @patch("role_voice.input.hotkey.keyboard")
    def test_stop_cleans_up(self, mock_kb: MagicMock) -> None:
        from role_voice.input.hotkey import HotkeyListener

        mock_kb.HotKey.parse.return_value = []
        callback = MagicMock()
        listener = HotkeyListener("<ctrl>+<shift>", callback)
        listener.start()
        listener.stop()
        # Should not raise

    def test_hotkey_str_property(self) -> None:
        with patch("role_voice.input.hotkey.keyboard") as mock_kb:
            mock_kb.HotKey.parse.return_value = []
            from role_voice.input.hotkey import HotkeyListener

            listener = HotkeyListener("<ctrl>+<shift>", lambda e: None)
            assert listener.hotkey_str == "<ctrl>+<shift>"
