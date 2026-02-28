# role-voice

Local push-to-talk voice interface for coding agents. Speak to Claude Code, execute terminal commands, or paste transcriptions -- all without cloud API calls.

## Features

- **Push-to-talk**: Hold a configurable hotkey to record, release to transcribe
- **100% local STT**: Uses [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) on Apple Silicon or [faster-whisper](https://github.com/SYSTRAN/faster-whisper) on other platforms
- **Multiple targets**: Clipboard, Claude Code CLI, or direct terminal input
- **Low latency**: Sub-second transcription with VAD silence trimming
- **Configurable**: YAML config with CLI overrides

## Quickstart

```bash
# Install (Apple Silicon)
pip install "role-voice[mlx,vad]"

# Install (Linux / NVIDIA)
pip install "role-voice[faster-whisper,vad]"

# Run with default settings (clipboard target, Ctrl+Shift hotkey)
role-voice run

# Run with Claude Code target
role-voice run --target claude-code

# Run with terminal paste target
role-voice run --target terminal
```

## How It Works

```
Hold hotkey → Record audio → Release hotkey → VAD trim → Local STT → Dispatch to target
```

1. **Press & hold** the push-to-talk hotkey (default: `Ctrl+Shift`)
2. **Speak** your command or text
3. **Release** the hotkey
4. Audio is trimmed (Silero VAD), transcribed locally (Whisper), and dispatched to your target

## Configuration

Create `~/.config/role-voice/config.yaml`:

```yaml
audio:
  sample_rate: 16000
  device: null               # null = system default

stt:
  engine: auto               # auto, mlx, or faster-whisper
  model: mlx-community/whisper-turbo
  language: en

hotkey:
  push_to_talk: "<ctrl>+<shift>"

target:
  type: clipboard            # clipboard, claude-code, terminal
  auto_execute: false        # terminal only: press Enter after paste

ui:
  show_transcription: true
  show_timing: true
```

See [docs/configuration.md](docs/configuration.md) for the full reference.

## CLI Commands

```bash
role-voice run              # Start push-to-talk loop
role-voice devices          # List audio input devices
role-voice config           # Show current configuration
role-voice benchmark        # Benchmark STT engine latency
role-voice --version        # Show version
```

## Requirements

- Python 3.11+
- macOS (Apple Silicon recommended) or Linux
- Microphone access permission
- Accessibility permission (macOS, for global hotkeys)

See [docs/installation.md](docs/installation.md) for platform-specific setup.

## Development

```bash
git clone https://github.com/yourusername/role-voice.git
cd role-voice
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest -m "not slow"

# Lint
ruff check .
ruff format --check .
```

See [docs/contributing.md](docs/contributing.md) for the full guide.

## Architecture

```
src/role_voice/
├── cli.py          # Typer CLI
├── app.py          # Main orchestrator
├── config.py       # Pydantic config models
├── audio/          # Recording + VAD preprocessing
├── stt/            # STT engines (mlx-whisper, faster-whisper)
├── input/          # Hotkey listener (pynput)
├── targets/        # Dispatchers (clipboard, claude-code, terminal)
└── ui/             # Rich console feedback
```

See [docs/architecture.md](docs/architecture.md) for details.

## License

MIT
