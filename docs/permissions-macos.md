# macOS Permissions

role-voice requires two macOS permissions to function correctly.

## Microphone Access

**Required for**: Recording audio from your microphone.

**When prompted**: The first time you run `role-voice run` or `role-voice devices`.

**How to grant**:
1. System Settings > Privacy & Security > Microphone
2. Enable the toggle for your terminal app (Terminal, iTerm2, etc.)

**If denied**: You'll see "Microphone access denied". Go to System Settings and toggle it on.

## Accessibility Access

**Required for**: Global hotkey detection (pynput) and terminal paste simulation (osascript).

**When prompted**: The first time pynput attempts to listen for global keyboard events.

**How to grant**:
1. System Settings > Privacy & Security > Accessibility
2. Click the "+" button and add your terminal app

**If hotkeys don't work**: The most common cause is missing Accessibility permission. Add your terminal app to the Accessibility list and restart role-voice.

## Troubleshooting

**Permission dialog doesn't appear**:
- Try removing your terminal app from the Microphone/Accessibility lists and re-adding it
- Restart your terminal app after granting permissions

**Using Python directly** (not from a terminal app):
- You may need to add the Python binary itself to the permission lists
- Find it with: `which python3`
