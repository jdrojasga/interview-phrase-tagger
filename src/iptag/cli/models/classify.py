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
    model: str = typer.Option(
        ZeroShotClassifier.DEFAULT_MODEL,
        "--model",
        help="HuggingFace model ID or local path.",
    ),
    threshold: Optional[float] = typer.Option(
        None, "--threshold", help="Override confidence threshold from config."
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Path to write JSON results. Prints to stdout if omitted.",
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

    results = [asdict(r) for r in transcription.metadata["classifications"]]

    if output:
        with open(output, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        typer.echo(f"Results written to {output}")
    else:
        for r in results:
            assigned = ", ".join(r["labels"]) if r["labels"] else "(none)"
            typer.echo(f"[{assigned}] {r['text']}")
