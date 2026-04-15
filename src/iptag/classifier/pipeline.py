"""Integration functions for classifying transcription data."""

from iptag.classifier.classifier import ZeroShotClassifier
from iptag.classifier.config import CategoriesConfig
from iptag.transcriptions.models import TranscriptionData
from iptag.utils.logging import get_logger

logger = get_logger(__name__)


def classify_transcription(
    transcription_data: TranscriptionData,
    classifier: ZeroShotClassifier,
    categories: CategoriesConfig,
) -> None:
    """Classify sentences in a transcription and store results in metadata.

    Reads sentences from ``metadata["sentences"]`` (produced by
    ``split_text_using_regex``), classifies each one, and stores the
    results in ``metadata["classifications"]``.

    Args:
        transcription_data: Transcription with sentences already split.
        classifier: A ZeroShotClassifier instance.
        categories: Categories configuration.

    Raises:
        ValueError: If no sentences are found in metadata.
    """
    sentences = transcription_data.metadata.get("sentences", [])
    if not sentences:
        raise ValueError(
            "No sentences found in metadata. Run split_text_using_regex first."
        )

    logger.info(
        f"Classifying {len(sentences)} sentences from '{transcription_data.source}'."
    )
    results = classifier.classify_batch(sentences, categories)
    transcription_data.metadata["classifications"] = results
    logger.info(f"Classification complete for '{transcription_data.source}'.")
