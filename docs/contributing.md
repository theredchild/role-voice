# Contributing

## Development Setup

```bash
git clone https://github.com/yourusername/role-voice.git
cd role-voice
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Running Tests

```bash
# Unit tests (no hardware/models needed)
pytest -m "not slow and not hardware" -v

# All tests including model loading
pytest -v

# With coverage
pytest --cov=role_voice --cov-report=html
```

## Code Style

- Python 3.11+
- All files must include `from __future__ import annotations`
- Line length: 120 characters
- Formatting: `ruff format`
- Linting: `ruff check`

```bash
# Auto-fix lint issues
ruff check --fix .

# Format code
ruff format .
```

## Project Structure

- `src/role_voice/` -- Source code (src layout)
- `tests/unit/` -- Unit tests (mocked, fast)
- `tests/integration/` -- Integration tests (require hardware/models)
- `scripts/` -- Development utilities
- `docs/` -- Documentation
- `config/` -- Default configuration files

## Adding a New Target

1. Create `src/role_voice/targets/my_target.py` implementing `TargetDispatcher`
2. Add a factory branch in `src/role_voice/targets/factory.py`
3. Add tests in `tests/unit/test_targets.py`
4. Document in `docs/configuration.md`

## Adding a New STT Engine

1. Create `src/role_voice/stt/my_engine.py` implementing `STTEngine`
2. Add a factory branch in `src/role_voice/stt/factory.py`
3. Add optional dependencies in `pyproject.toml`
4. Add tests in `tests/unit/test_stt.py`
