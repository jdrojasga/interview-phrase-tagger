"""Smoke tests for the presentation package."""

import pytest
from rich.console import Console

from iptag.classifier.models import ClassificationResult
from iptag.presentation.colors import css_class, html_color, terminal_color
from iptag.presentation.html import render_to_html
from iptag.presentation.segments import build_segments, category_counts
from iptag.presentation.terminal import render_to_terminal
from iptag.transcriptions.models import TranscriptionData


def _make_transcription() -> TranscriptionData:
    t = TranscriptionData(text="one two three", source="sample.txt")
    t.metadata["sentences"] = ["one", "two", "three"]
    t.metadata["classifications"] = [
        ClassificationResult(
            text="one", labels=["alpha"], scores={"alpha": 0.9}, index=0
        ),
        ClassificationResult(text="two", labels=[], scores={"alpha": 0.1}, index=1),
        ClassificationResult(
            text="three",
            labels=["alpha", "beta"],
            scores={"alpha": 0.8, "beta": 0.7},
            index=2,
        ),
    ]
    return t


@pytest.mark.unit
def test_color_helpers_are_deterministic() -> None:
    """Same label always maps to the same color + class."""
    assert terminal_color("alpha") == terminal_color("alpha")
    assert html_color("alpha") == html_color("alpha")
    assert css_class("Hello World!") == "cat-hello-world-"


@pytest.mark.unit
def test_build_segments_preserves_order_and_labels() -> None:
    """Segments keep sentence order and labels."""
    t = _make_transcription()
    segs = [s for s in build_segments(t) if s.text.strip()]
    assert [s.text for s in segs] == ["one", "two", "three"]
    assert segs[0].labels == ["alpha"]
    assert segs[1].labels == []
    assert segs[2].labels == ["alpha", "beta"]


@pytest.mark.unit
def test_category_counts_aggregates() -> None:
    """Per-category count + avg score match expected values."""
    counts = category_counts(_make_transcription())
    assert counts["alpha"] == {"count": 2, "avg_score": pytest.approx(0.85)}
    assert counts["beta"] == {"count": 1, "avg_score": pytest.approx(0.7)}


@pytest.mark.unit
def test_render_to_html_writes_marks(tmp_path) -> None:
    """HTML output contains one <mark> per classified sentence and filter cards."""
    out = tmp_path / "out.html"
    render_to_html(_make_transcription(), out)
    content = out.read_text(encoding="utf-8")
    # All 3 classified sentences get a <mark data-idx=...> element
    assert content.count("<mark ") == 3
    # Category names appear in embedded JS data and CSS
    assert "cat-alpha" in content
    assert "cat-beta" in content
    # Filter cards use data-name with the category name
    assert 'data-name="alpha"' in content


@pytest.mark.unit
def test_render_to_terminal_runs() -> None:
    """Terminal renderer emits the transcript text and category names."""
    console = Console(record=True, width=80)
    render_to_terminal(_make_transcription(), console=console)
    exported = console.export_text()
    assert "one" in exported
    assert "alpha" in exported
