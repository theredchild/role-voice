# Architecture

## Module Dependency Diagram

```
cli.py
  └── app.py (orchestrator)
        ├── audio/capture.py      ← sounddevice
        ├── audio/preprocessing.py ← silero-vad
        ├── stt/factory.py
        │   ├── stt/mlx_engine.py  ← mlx-whisper
        │   └── stt/faster_whisper_engine.py ← faster-whisper
        ├── input/hotkey.py        ← pynput
        ├── targets/factory.py
        │   ├── targets/clipboard.py
        │   ├── targets/claude_code.py
        │   └── targets/terminal.py
        └── ui/console.py          ← rich
```

## Data Flow

```
1. User holds hotkey
2. pynput fires PRESSED → app starts AudioCapture
3. sounddevice callback accumulates chunks into AudioBuffer
4. User releases hotkey
5. pynput fires RELEASED → app stops AudioCapture
6. Background thread:
   a. AudioBuffer.to_array() → contiguous numpy array
   b. AudioPreprocessor: VAD trim + normalize
   c. STTEngine.transcribe() → TranscriptionResult
   d. ConsoleUI.show_result()
   e. TargetDispatcher.dispatch(text)
7. Ready for next cycle
```

## Threading Model

- **Main thread**: Runs the event loop (`threading.Event().wait()`)
- **pynput thread**: Keyboard listener (daemon thread)
- **PortAudio thread**: Audio callback (managed by sounddevice)
- **Processing thread**: Spawned per recording for STT + dispatch (daemon)
- **Processing lock**: Prevents concurrent transcriptions (models aren't thread-safe)

## Adding a New STT Engine

1. Create `src/role_voice/stt/my_engine.py`
2. Implement the `STTEngine` ABC from `stt/base.py`
3. Add a branch in `stt/factory.py`
4. Add an optional dependency group in `pyproject.toml`

## Adding a New Target

1. Create `src/role_voice/targets/my_target.py`
2. Implement the `TargetDispatcher` ABC from `targets/base.py`
3. Add a branch in `targets/factory.py`
