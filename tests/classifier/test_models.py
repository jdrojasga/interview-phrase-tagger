"""Tests for classification result models."""

import pytest

from iptag.classifier.models import ClassificationResult


@pytest.mark.unit
class TestClassificationResult:
    """Tests for ClassificationResult dataclass."""

    def test_create_result(self):
        """Test creating a result with all fields."""
        result = ClassificationResult(
            text="Hola mundo",
            labels=["saludo"],
            scores={"saludo": 0.9, "despedida": 0.1},
            index=0,
        )
        assert result.text == "Hola mundo"
        assert result.labels == ["saludo"]
        assert result.scores["saludo"] == 0.9
        assert result.index == 0

    def test_defaults(self):
        """Test default values for optional fields."""
        result = ClassificationResult(text="test", labels=[])
        assert result.scores == {}
        assert result.index == 0

    def test_empty_labels(self):
        """Test result with no assigned labels."""
        result = ClassificationResult(
            text="nada relevante",
            labels=[],
            scores={"a": 0.1},
        )
        assert result.labels == []
