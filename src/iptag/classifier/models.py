"""Data models for classification results."""

from dataclasses import dataclass, field


@dataclass
class ClassificationResult:
    """Result of classifying a single text segment."""

    text: str
    labels: list[str]
    scores: dict[str, float] = field(default_factory=dict)
    index: int = 0
