"""CLI command for classifying transcription text."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

import typer

from iptag.classifier import (
    ZeroShotClassifier,
    classify_transcription,
    load_categories_from_yaml,
)
from iptag.presentation import render_to_html, render_to_terminal
from iptag.transcriptions.loader import (
    TranscriptionLoaderConfig,
    TranscriptionLoaderFactory,
)
from iptag.transcriptions.splitter.text import split_text_using_regex


def classify(
    input_file: Path = typer.Option(
        ..., "--input", help="Path to the input text file."
    ),
    categories_file: Path = typer.Option(
        ..., "--categories", help="Path to the categories YAML config."
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        help="Catalog alias ('fast', 'balanced', 'accurate') or HuggingFace model ID. Defaults to CLASSIFIER_MODEL env var (or 'balanced').",
    ),
    threshold: Optional[float] = typer.Option(
        None, "--threshold", help="Override confidence threshold from config."
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Path to write JSON results. If omitted, no JSON is written.",
    ),
    html: Optional[Path] = typer.Option(
        None,
        "--html",
        help="Path to write a standalone HTML report.",
    ),
) -> None:
    """Classify sentences in a transcription by topic categories."""
    categories = load_categories_from_yaml(categories_file)
    if threshold is not None:
        categories.threshold = threshold

    config = TranscriptionLoaderConfig(type="txt", parameters={"encoding": "utf-8"})
    loader = TranscriptionLoaderFactory.from_config(config)
    transcription = loader.load(input_file)

    split_text_using_regex(transcription)

    classifier = ZeroShotClassifier(model_name_or_path=model)
    classify_transcription(transcription, classifier, categories)

    render_to_terminal(transcription)

    if output:
        results = [asdict(r) for r in transcription.metadata["classifications"]]
        with open(output, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        typer.echo(f"Results written to {output}")

    if html:
        render_to_html(transcription, html, categories=categories)
        typer.echo(f"HTML report written to {html}")
