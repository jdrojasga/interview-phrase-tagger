"""Command to handle model-related operations in the Interview Phrase Tagger CLI."""

import typer

from iptag.cli.models.classify import classify

app = typer.Typer(help="Model-related commands for Interview Phrase Tagger CLI")
app.command()(classify)
