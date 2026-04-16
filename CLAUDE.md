# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A toolkit for tagging/underlining phrases in interview transcripts by configurable topics. Goals: segment transcripts, assign multi-label topics, export annotated text, run offline with CPU-friendly models.

Currently in early prototype/WIP stage.

## Commands

All commands use `uv run` as the package manager.

```bash
# Install dependencies
uv sync

# Run the CLI
uv run iptag

# Run all tests
uv run pytest

# Run tests by marker
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m "not slow"

# Run a single test file
uv run pytest tests/test_example.py

# Lint and format
uv run ruff check .
uv run ruff format .

# Run example data loading script
uv run python scripts/load_data.py
```

## Architecture

### Transcription Loader System

The loader uses a **factory + plugin registration pattern**:

1. `TranscriptionLoader` (abstract, `loader/base.py`) — defines `load()`, `load_multiple()`, `validate_source()` interface. Inherits `LoggerMixin`.
2. `TranscriptionLoaderFactory` (`loader/factory.py`) — holds a class-level registry. Loaders self-register via the `@register("type_name")` decorator.
3. `TranscriptionLoaderConfig` (`loader/config.py`) — Pydantic model with `type` and `parameters` fields. Passed to `factory.from_config()` to instantiate the right loader.
4. Implementations in `loader/implementations/` — `TxtTranscriptionLoader` (functional), `GDocsTranscriptionLoader` (placeholder, raises `NotImplementedError`).

To add a new loader, create a new file in `implementations/`, apply `@TranscriptionLoaderFactory.register("your_type")` to the class, and import it somewhere so it self-registers.

### Text Splitter

`splitter/text.py` — `split_text_using_regex()` takes a `TranscriptionData` and a regex pattern, splits the text, and stores results in `metadata["sentences"]`.

### Logging

`utils/logging.py` provides `LoggerMixin` (used as a mixin on loader classes) and `get_logger()`/`get_logger_for()` helpers. Log level is set by `IptagSettings.debug` from the `.env` file.

### CLI

Typer app (`cli/__init__.py`) with two subcommand groups: `data` and `models`. Both are mostly placeholders. Entry point: `iptag`.

## Test Markers

Defined in `pyproject.toml` with `--strict-markers`:
- `unit` — isolated, fast tests
- `integration` — cross-component tests
- `slow` — time-consuming tests
