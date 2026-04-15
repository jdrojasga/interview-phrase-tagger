"""Render a classified transcription to the terminal with `rich`."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from iptag.presentation.colors import terminal_color
from iptag.presentation.segments import (
    all_labels,
    build_segments,
    category_counts,
)
from iptag.transcriptions.models import TranscriptionData


def render_to_terminal(
    transcription: TranscriptionData, console: Console | None = None
) -> None:
    """Print the full transcript with classified phrases highlighted."""
    console = console or Console()

    source = transcription.source or "transcription"
    console.print(
        Panel(_build_transcript_text(transcription), title=source, border_style="dim")
    )
    console.print(_build_legend(transcription))
    console.print(_build_summary(transcription))


def _build_transcript_text(transcription: TranscriptionData) -> Text:
    text = Text()
    for seg in build_segments(transcription):
        if not seg.labels:
            text.append(seg.text)
            continue
        color = terminal_color(seg.labels[0])
        style = f"black on {color} underline"
        text.append(seg.text, style=style)
        if len(seg.labels) > 1:
            extras = ",".join(seg.labels[1:])
            text.append(f" [+{extras}]", style="dim italic")
    return text


def _build_legend(transcription: TranscriptionData) -> Table:
    table = Table(title="Legend", show_header=False, border_style="dim", pad_edge=False)
    table.add_column("swatch", no_wrap=True)
    table.add_column("category")
    for label in all_labels(transcription):
        swatch = Text("  ", style=f"on {terminal_color(label)}")
        table.add_row(swatch, label)
    return table


def _build_summary(transcription: TranscriptionData) -> Table:
    table = Table(title="Summary", border_style="dim")
    table.add_column("category")
    table.add_column("count", justify="right")
    table.add_column("avg score", justify="right")
    for label, stats in sorted(
        category_counts(transcription).items(),
        key=lambda kv: (-kv[1]["count"], kv[0]),
    ):
        color = terminal_color(label)
        table.add_row(
            Text(label, style=color),
            str(stats["count"]),
            f"{stats['avg_score']:.2f}",
        )
    return table
