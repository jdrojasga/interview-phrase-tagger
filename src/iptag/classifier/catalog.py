"""Catalog of supported zero-shot classification models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelEntry:
    model_id: str
    description: str
    size_mb: int


CATALOG: dict[str, ModelEntry] = {
    "fast": ModelEntry(
        model_id="MoritzLaurer/mdeberta-v3-small-mnli",
        description="Fastest inference, minimal accuracy gain over baseline (~3-5%)",
        size_mb=133,
    ),
    "balanced": ModelEntry(
        model_id="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
        description="Best balance of accuracy and speed (~5-10% gain over baseline)",
        size_mb=440,
    ),
    "accurate": ModelEntry(
        model_id="facebook/bart-large-mnli",
        description="Highest accuracy, slower inference (~8-12% gain over baseline)",
        size_mb=1600,
    ),
}

DEFAULT_ALIAS = "balanced"


def resolve_model(alias_or_id: str) -> str:
    """Resolve a catalog alias to a HuggingFace model ID, or pass through as-is."""
    entry = CATALOG.get(alias_or_id)
    return entry.model_id if entry else alias_or_id
