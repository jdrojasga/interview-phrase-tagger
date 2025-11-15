"""Preprocess command for the Interview Phrase Tagger."""

import typer
from pydantic import BaseModel


class PreprocessConfig(BaseModel):
    """Configuration for the preprocess command."""

    input_file: str
    output_file: str


def preprocess(
    input_file: str = typer.Option(..., help="Path to the input data file."),
    output_file: str = typer.Option(
        ..., help="Path to save the preprocessed data file."
    ),
):
    """Preprocess the input data file and save the result."""
    config = PreprocessConfig(
        input_file=input_file,
        output_file=output_file,
    )
    # Placeholder for preprocessing logic
    typer.echo(f"Preprocessing {config.input_file} and saving to {config.output_file}")
