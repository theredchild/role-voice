from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from role_voice.stt.base import TranscriptionResult


class ConsoleUI:
    """Rich-based console feedback for recording and transcription states."""

    def __init__(self, show_transcription: bool = True, show_timing: bool = True):
        self._console = Console()
        self._show_transcription = show_transcription
        self._show_timing = show_timing

    def show_ready(self, hotkey: str, target: str, engine: str) -> None:
        self._console.print(
            Panel(
                f"[bold green]Ready[/] | Hotkey: [cyan]{hotkey}[/] | "
                f"Target: [yellow]{target}[/] | Engine: [dim]{engine}[/]\n"
                f"[dim]Hold the hotkey to record, release to transcribe. Ctrl+C to quit.[/]",
                title="[bold]role-voice[/]",
            )
        )

    def show_recording(self) -> None:
        self._console.print("[bold red]  Recording...[/]", end="\r")

    def show_processing(self) -> None:
        self._console.print("[bold yellow]  Transcribing...[/]", end="\r")

    def show_result(self, result: TranscriptionResult) -> None:
        if self._show_transcription:
            self._console.print(f"\r[bold green]>[/] {result.text}")
        if self._show_timing:
            rtf = result.processing_seconds / max(result.duration_seconds, 0.001)
            self._console.print(
                f"  [dim]Audio: {result.duration_seconds:.1f}s | "
                f"STT: {result.processing_seconds:.2f}s | "
                f"RTF: {rtf:.2f}x[/]"
            )

    def show_error(self, message: str) -> None:
        self._console.print(f"[bold red]Error:[/] {message}")

    def show_empty_recording(self) -> None:
        self._console.print("\r[dim]No speech detected, skipping.[/]")

    def show_loading(self, message: str) -> None:
        self._console.print(f"[bold blue]  {message}[/]")
