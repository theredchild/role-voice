# Configuration

role-voice reads configuration from `~/.config/role-voice/config.yaml`. All values have sensible defaults.

## Full Reference

```yaml
audio:
  sample_rate: 16000        # Recording sample rate in Hz (Whisper expects 16kHz)
  channels: 1               # Number of channels (1 = mono)
  block_size: 1024           # Samples per audio callback (~64ms at 16kHz)
  device: null               # Audio device: null (system default), index, or name substring

vad:
  enabled: true              # Enable voice activity detection (silence trimming)
  threshold: 0.5             # Speech probability threshold (0.0 to 1.0)
  min_speech_duration_ms: 250   # Ignore speech segments shorter than this
  min_silence_duration_ms: 100  # Merge speech segments separated by less than this

stt:
  engine: auto               # STT engine: "auto", "mlx", "faster-whisper"
  model: mlx-community/whisper-turbo   # Model name/path
  language: en               # Language code or null for auto-detect
  device: cpu                # faster-whisper only: "cpu" or "cuda"
  compute_type: int8         # faster-whisper only: "int8", "float16", "float32"

hotkey:
  push_to_talk: "<ctrl>+<shift>"   # pynput hotkey format

target:
  type: clipboard            # Target: "clipboard", "claude-code", "terminal"
  auto_execute: false        # Terminal target only: press Enter after pasting
  claude_args: []            # Extra arguments passed to `claude -p`

ui:
  show_transcription: true   # Print transcribed text to console
  show_timing: true          # Print timing statistics
```

## CLI Overrides

```bash
role-voice run --target terminal --hotkey "<cmd>+<shift>" --engine mlx
```

## Hotkey Format

Uses [pynput hotkey syntax](https://pynput.readthedocs.io/):

| Hotkey | Format |
|--------|--------|
| Ctrl+Shift | `<ctrl>+<shift>` |
| Cmd+Shift (macOS) | `<cmd>+<shift>` |
| Ctrl+Space | `<ctrl>+<space>` |
| F13 | `<f13>` |
| Right Alt | `<right_alt>` |

## Engine Selection

| Platform | `auto` resolves to | Recommended model |
|----------|-------------------|-------------------|
| macOS Apple Silicon | `mlx` | `mlx-community/whisper-turbo` |
| macOS Intel | `faster-whisper` | `base.en` |
| Linux (CPU) | `faster-whisper` | `base.en` |
| Linux (NVIDIA GPU) | `faster-whisper` | `small.en` with `device: cuda` |
