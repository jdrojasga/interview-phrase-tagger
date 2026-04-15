"""Tests for classifier configuration models."""

import pytest
import yaml

from iptag.classifier.config import (
    CategoriesConfig,
    CategoryDefinition,
    load_categories_from_yaml,
)


@pytest.mark.unit
class TestCategoryDefinition:
    """Tests for CategoryDefinition model."""

    def test_create_with_required_fields(self):
        """Test creating a category with only required fields."""
        cat = CategoryDefinition(name="trabajo", label="experiencia laboral")
        assert cat.name == "trabajo"
        assert cat.label == "experiencia laboral"
        assert cat.description is None

    def test_create_with_description(self):
        """Test creating a category with an optional description."""
        cat = CategoryDefinition(
            name="trabajo",
            label="experiencia laboral",
            description="Sobre trabajos previos",
        )
        assert cat.description == "Sobre trabajos previos"


@pytest.mark.unit
class TestCategoriesConfig:
    """Tests for CategoriesConfig model."""

    def test_defaults(self):
        """Test default values for hypothesis template and threshold."""
        config = CategoriesConfig(categories=[CategoryDefinition(name="a", label="A")])
        assert config.hypothesis_template == "Este texto trata sobre {}."
        assert config.threshold == 0.5

    def test_custom_threshold(self):
        """Test setting a custom threshold."""
        config = CategoriesConfig(
            categories=[CategoryDefinition(name="a", label="A")],
            threshold=0.7,
        )
        assert config.threshold == 0.7

    def test_multiple_categories(self):
        """Test config with multiple categories."""
        cats = [
            CategoryDefinition(name="a", label="A"),
            CategoryDefinition(name="b", label="B"),
        ]
        config = CategoriesConfig(categories=cats)
        assert len(config.categories) == 2


@pytest.mark.unit
class TestLoadCategoriesFromYaml:
    """Tests for YAML loading."""

    def test_load_valid_yaml(self, tmp_path):
        """Test loading a valid YAML categories file."""
        data = {
            "hypothesis_template": "Trata sobre {}.",
            "threshold": 0.6,
            "categories": [
                {"name": "edu", "label": "educacion"},
                {"name": "trabajo", "label": "empleo", "description": "desc"},
            ],
        }
        yaml_path = tmp_path / "cats.yaml"
        yaml_path.write_text(yaml.dump(data))

        config = load_categories_from_yaml(yaml_path)
        assert len(config.categories) == 2
        assert config.threshold == 0.6
        assert config.categories[1].description == "desc"

    def test_load_missing_file(self, tmp_path):
        """Test that a missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_categories_from_yaml(tmp_path / "missing.yaml")
