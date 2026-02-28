# Installation

## Prerequisites

- Python 3.11 or later
- A working microphone

## macOS (Apple Silicon) -- Recommended

```bash
pip install "role-voice[mlx,vad]"
```

This installs:
- `mlx-whisper` for Apple Silicon-optimized STT
- `silero-vad` for voice activity detection

### Permissions

**Microphone**: On first run, macOS will ask for microphone permission for your terminal app. Grant it in System Settings > Privacy & Security > Microphone.

**Accessibility**: Global hotkeys require Accessibility permission. Grant it to your terminal app in System Settings > Privacy & Security > Accessibility.

## Linux

```bash
pip install "role-voice[faster-whisper,vad]"
```

System dependencies:
```bash
# Debian/Ubuntu
sudo apt install libportaudio2 xdotool xclip

# Fedora
sudo dnf install portaudio xdotool xclip
```

## From Source

```bash
git clone https://github.com/yourusername/role-voice.git
cd role-voice
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Verify Installation

```bash
# Check version
role-voice --version

# List audio devices
role-voice devices

# Test microphone
python scripts/test_microphone.py
```
