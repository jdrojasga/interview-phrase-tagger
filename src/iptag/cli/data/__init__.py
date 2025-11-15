"""Command to handle data-related operations in the Interview Phrase Tagger CLI."""

import typer

from .preprocess import preprocess

app = typer.Typer(help="Data-related commands for Interview Phrase Tagger CLI")
app.command()(preprocess)
