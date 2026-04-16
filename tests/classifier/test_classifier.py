"""Integration tests for ZeroShotClassifier (requires model download)."""

import pytest

from iptag.classifier.classifier import ZeroShotClassifier
from iptag.classifier.config import (
    CategoriesConfig,
    CategoryDefinition,
    SubcategoryDefinition,
)


@pytest.fixture
def sample_categories():
    """Sample categories for testing."""
    return CategoriesConfig(
        categories=[
            CategoryDefinition(
                name="saludo",
                label="saludo y presentacion",
                subcategories=[
                    SubcategoryDefinition(name="saludo", label="saludo y presentacion"),
                ],
            ),
            CategoryDefinition(
                name="animales",
                label="animales y mascotas",
                subcategories=[
                    SubcategoryDefinition(name="animales", label="animales y mascotas"),
                ],
            ),
            CategoryDefinition(
                name="trabajo",
                label="experiencia laboral",
                subcategories=[
                    SubcategoryDefinition(name="trabajo", label="experiencia laboral"),
                ],
            ),
        ],
        threshold=0.5,
    )


@pytest.mark.slow
@pytest.mark.integration
class TestZeroShotClassifier:
    """Integration tests that load and run the actual model."""

    def test_classify_single(self, sample_categories):
        """Test classifying a single sentence."""
        classifier = ZeroShotClassifier()
        result = classifier.classify(
            "Hola, como estas? Mucho gusto en conocerte.",
            sample_categories,
        )
        assert "saludo" in result.labels
        assert len(result.scores) == 3

    def test_classify_batch(self, sample_categories):
        """Test classifying a batch of sentences."""
        classifier = ZeroShotClassifier()
        texts = [
            "Buenos dias, me presento",
            "Mi gato se llama Lennon",
        ]
        results = classifier.classify_batch(texts, sample_categories)
        assert len(results) == 2
        assert results[0].index == 0
        assert results[1].index == 1

    def test_scores_are_floats(self, sample_categories):
        """Test that all scores are float values."""
        classifier = ZeroShotClassifier()
        result = classifier.classify("Texto de prueba", sample_categories)
        for score in result.scores.values():
            assert isinstance(score, float)
