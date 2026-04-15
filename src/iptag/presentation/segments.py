"""Build ordered text segments from a classified transcription."""

from dataclasses import dataclass

from iptag.transcriptions.models import TranscriptionData


@dataclass
class Segment:
    """A run of text with the labels (if any) assigned to it."""

    text: str
    labels: list[str]


def build_segments(transcription: TranscriptionData) -> list[Segment]:
    """Return ordered segments combining sentences and their classifications.

    The splitter drops the delimiters, so we rejoin sentences with a single
    space — good enough for presentation. Sentences without any labels are
    still emitted so the full transcript is visible.
    """
    results = transcription.metadata.get("classifications", [])
    segments: list[Segment] = []
    for i, result in enumerate(results):
        if i > 0:
            segments.append(Segment(text=" ", labels=[]))
        segments.append(Segment(text=result.text, labels=list(result.labels)))
    return segments


def category_counts(transcription: TranscriptionData) -> dict[str, dict[str, float]]:
    """Return per-category ``{count, avg_score}`` for classified sentences."""
    results = transcription.metadata.get("classifications", [])
    stats: dict[str, dict[str, float]] = {}
    for r in results:
        for label in r.labels:
            entry = stats.setdefault(label, {"count": 0.0, "score_sum": 0.0})
            entry["count"] += 1
            entry["score_sum"] += r.scores.get(label, 0.0)
    return {
        label: {
            "count": int(v["count"]),
            "avg_score": v["score_sum"] / v["count"] if v["count"] else 0.0,
        }
        for label, v in stats.items()
    }


def all_labels(transcription: TranscriptionData) -> list[str]:
    """Return every label that was assigned at least once, in first-seen order."""
    seen: list[str] = []
    for r in transcription.metadata.get("classifications", []):
        for label in r.labels:
            if label not in seen:
                seen.append(label)
    return seen
