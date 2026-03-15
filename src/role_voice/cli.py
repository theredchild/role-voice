from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from role_voice import __version__
from role_voice.config import AppConfig, load_config

app = typer.Typer(
    name="role-voice",
    help="Local push-to-talk voice interface for coding agents.",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"role-voice {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show version."),
    ] = None,
) -> None:
    """role-voice: Push-to-talk voice interface for coding agents."""


@app.command()
def run(
    config_path: Annotated[
        Path | None,
        typer.Option("--config", "-c", help="Path to config YAML file."),
    ] = None,
    target: Annotated[
        str | None,
        typer.Option("--target", "-t", help="Target: clipboard, claude-code, terminal."),
    ] = None,
    hotkey: Annotated[
        str | None,
        typer.Option("--hotkey", "-k", help="Push-to-talk hotkey (pynput format)."),
    ] = None,
    engine: Annotated[
        str | None,
        typer.Option("--engine", "-e", help="STT engine: auto, mlx, faster-whisper."),
    ] = None,
    model: Annotated[
        str | None,
        typer.Option("--model", "-m", help="STT model name/size."),
    ] = None,
) -> None:
    """Start the push-to-talk voice interface."""
    config, config_used = load_config(config_path)

    if config_used:
        console.print(f"[dim]Config: {config_used}[/]")

    if target:
        config.target.type = target
    if hotkey:
        config.hotkey.push_to_talk = hotkey
    if engine:
        config.stt.engine = engine
    if model:
        config.stt.model = model

    from role_voice.app import RoleVoiceApp

    app_instance = RoleVoiceApp(config)
    app_instance.run()


@app.command()
def devices() -> None:
    """List available audio input devices."""
    import sounddevice as sd

    devices_list = sd.query_devices()
    table = Table(title="Audio Input Devices")
    table.add_column("Index", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Channels", justify="right")
    table.add_column("Sample Rate", justify="right")
    table.add_column("Default", justify="center")

    default_input = sd.default.device[0]

    for i, dev in enumerate(devices_list):
        if dev["max_input_channels"] > 0:
            is_default = "* " if i == default_input else ""
            table.add_row(
                str(i),
                dev["name"],
                str(dev["max_input_channels"]),
                f"{dev['default_samplerate']:.0f}",
                is_default,
            )

    console.print(table)


@app.command()
def config(
    config_path: Annotated[
        Path | None,
        typer.Option("--config", "-c", help="Path to config YAML file."),
    ] = None,
) -> None:
    """Show current configuration."""
    cfg, config_used = load_config(config_path)
    if config_used:
        console.print(f"[dim]Loaded from: {config_used}[/]\n")
    else:
        console.print("[dim]Using built-in defaults[/]\n")
    console.print_json(cfg.model_dump_json(indent=2))


@app.command()
def benchmark(
    engine: Annotated[
        str | None,
        typer.Option("--engine", "-e", help="STT engine to benchmark."),
    ] = None,
    duration: Annotated[
        float,
        typer.Option("--duration", "-d", help="Audio duration in seconds."),
    ] = 5.0,
) -> None:
    """Benchmark STT engine latency with synthetic audio."""
    import numpy as np

    config = AppConfig()
    if engine:
        config.stt.engine = engine

    from role_voice.stt.factory import create_stt_engine

    stt = create_stt_engine(config.stt)

    console.print(f"[bold]Benchmarking:[/] {stt.engine_name}")
    console.print("Loading model...")
    stt.load_model()

    samples = int(duration * 16000)
    audio = np.random.randn(samples).astype(np.float32) * 0.01

    console.print(f"Transcribing {duration}s of audio...")
    result = stt.transcribe(audio, sample_rate=16000)

    rtf = result.processing_seconds / max(result.duration_seconds, 0.001)
    console.print(f"[green]Done![/] STT took {result.processing_seconds:.2f}s (RTF: {rtf:.2f}x)")
