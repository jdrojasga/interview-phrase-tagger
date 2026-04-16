"""Tests for the classify_transcription pipeline function."""

from unittest.mock import MagicMock

import pytest

from iptag.classifier.config import (
    CategoriesConfig,
    CategoryDefinition,
    SubcategoryDefinition,
)
from iptag.classifier.models import ClassificationResult
from iptag.classifier.pipeline import classify_transcription
from iptag.transcriptions.models import TranscriptionData


@pytest.fixture
def transcription_with_sentences():
    """TranscriptionData with pre-split sentences."""
    td = TranscriptionData(
        text="Hola mundo. Adios mundo.",
        source="test.txt",
        metadata={"sentences": ["Hola mundo", "Adios mundo"]},
    )
    return td


@pytest.fixture
def sample_categories():
    """Sample categories config."""
    return CategoriesConfig(
        categories=[
            CategoryDefinition(
                name="saludo",
                label="saludo",
                subcategories=[SubcategoryDefinition(name="saludo", label="saludo")],
            ),
            CategoryDefinition(
                name="despedida",
                label="despedida",
                subcategories=[
                    SubcategoryDefinition(name="despedida", label="despedida"),
                ],
            ),
        ],
    )


@pytest.fixture
def mock_classifier():
    """Mock classifier that returns predictable results."""
    classifier = MagicMock()
    classifier.classify_batch.return_value = [
        ClassificationResult(
            text="Hola mundo",
            labels=["saludo"],
            scores={"saludo": 0.9, "despedida": 0.1},
            index=0,
        ),
        ClassificationResult(
            text="Adios mundo",
            labels=["despedida"],
            scores={"saludo": 0.2, "despedida": 0.8},
            index=1,
        ),
    ]
    return classifier


@pytest.mark.unit
class TestClassifyTranscription:
    """Tests for classify_transcription function."""

    def test_stores_results_in_metadata(
        self, transcription_with_sentences, mock_classifier, sample_categories
    ):
        """Test that results are stored in metadata['classifications']."""
        classify_transcription(
            transcription_with_sentences, mock_classifier, sample_categories
        )
        assert "classifications" in transcription_with_sentences.metadata
        assert len(transcription_with_sentences.metadata["classifications"]) == 2

    def test_raises_without_sentences(self, mock_classifier, sample_categories):
        """Test that ValueError is raised when sentences are missing."""
        td = TranscriptionData(text="No sentences", source="test.txt")
        with pytest.raises(ValueError, match="No sentences found"):
            classify_transcription(td, mock_classifier, sample_categories)

    def test_calls_classifier_with_sentences(
        self, transcription_with_sentences, mock_classifier, sample_categories
    ):
        """Test that the classifier is called with the correct sentences."""
        classify_transcription(
            transcription_with_sentences, mock_classifier, sample_categories
        )
        mock_classifier.classify_batch.assert_called_once_with(
            ["Hola mundo", "Adios mundo"], sample_categories
        )
