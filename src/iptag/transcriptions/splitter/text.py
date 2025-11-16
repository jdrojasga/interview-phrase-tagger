"""Splitter text transcription module.

In this module, we define classes and functions to handle text-based
transcription splitting. This includes functionality to split transcriptions
based on various criteria such as sentences, paragraphs, or custom delimiters.
"""

import re

from iptag.transcriptions.models import TranscriptionData
from iptag.utils.logging import get_logger

logger = get_logger(__name__)


def split_text_using_regex(
    transcription_data: TranscriptionData, regex: str = r"[.!?]+\s+"
) -> None:
    """Split transcription data text into sentences.

    This function modifies the transcription_data in place, adding a list of
    sentences to its metadata. The splitting is done based on the provided regex
    pattern.

    Args:
        transcription_data: The transcription data to add sentences to.
        regex: The regex pattern to use for splitting. Defaults to splitting on
            sentence-ending punctuation.
    """
    logger.debug(f"Splitting transcription {transcription_data.source} into sentences.")
    # Simple sentence splitter using regex
    sentence_endings = re.compile(regex)
    sentences = sentence_endings.split(transcription_data.text.strip())
    transcription_data.metadata["sentences"] = sentences
    logger.debug(
        f"Transcription {transcription_data.source} split into {len(sentences)}"
        " sentences."
    )
    return None
