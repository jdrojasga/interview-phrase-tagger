"""Tests for classifier configuration models."""

import pytest
import yaml
from pydantic import ValidationError

from iptag.classifier.config import (
    CategoriesConfig,
    CategoryDefinition,
    SubcategoryDefinition,
    load_categories_from_yaml,
)


@pytest.mark.unit
class TestSubcategoryDefinition:
    """Tests for SubcategoryDefinition model."""

    def test_create_with_required_fields(self):
        """Test creating a SubcategoryDefinition with only required fields."""
        sub = SubcategoryDefinition(name="trabajo", label="experiencia laboral")
        assert sub.name == "trabajo"
        assert sub.label == "experiencia laboral"
        assert sub.description is None

    def test_create_with_description(self):
        """Test creating a SubcategoryDefinition with an optional description."""
        sub = SubcategoryDefinition(
            name="trabajo",
            label="experiencia laboral",
            description="Sobre trabajos previos",
        )
        assert sub.description == "Sobre trabajos previos"


@pytest.mark.unit
class TestCategoryDefinition:
    """Tests for CategoryDefinition model."""

    def test_create_with_required_fields(self):
        """Test creating a CategoryDefinition with only required fields."""
        cat = CategoryDefinition(
            name="experiencia",
            label="Experiencia",
            subcategories=[SubcategoryDefinition(name="trabajo", label="empleo")],
        )
        assert cat.name == "experiencia"
        assert cat.label == "Experiencia"
        assert cat.description is None
        assert len(cat.subcategories) == 1

    def test_create_with_description(self):
        """Test creating a CategoryDefinition with an optional description."""
        cat = CategoryDefinition(
            name="experiencia",
            label="Experiencia",
            description="Grupo de experiencia",
            subcategories=[SubcategoryDefinition(name="trabajo", label="empleo")],
        )
        assert cat.description == "Grupo de experiencia"

    def test_subcategories_required(self):
        """Test that subcategories field is required."""
        with pytest.raises(ValidationError):
            CategoryDefinition(name="experiencia", label="Experiencia")


@pytest.mark.unit
class TestCategoriesConfig:
    """Tests for CategoriesConfig model."""

    def _make_config(self, **kwargs):
        cats = [
            CategoryDefinition(
                name="experiencia",
                label="Experiencia",
                subcategories=[
                    SubcategoryDefinition(name="trabajo", label="empleo"),
                    SubcategoryDefinition(name="educacion", label="estudios"),
                ],
            ),
            CategoryDefinition(
                name="competencias",
                label="Competencias",
                subcategories=[
                    SubcategoryDefinition(name="habilidades", label="skills"),
                ],
            ),
        ]
        return CategoriesConfig(categories=cats, **kwargs)

    def test_defaults(self):
        """Test that CategoriesConfig has correct default values."""
        config = self._make_config()
        assert config.hypothesis_template == "Este texto trata sobre {}."
        assert config.threshold == 0.5

    def test_custom_threshold(self):
        """Test setting a custom threshold value."""
        config = self._make_config(threshold=0.7)
        assert config.threshold == 0.7

    def test_multiple_categories(self):
        """Test that multiple categories are stored correctly."""
        config = self._make_config()
        assert len(config.categories) == 2

    def test_all_subcategories_returns_flat_list(self):
        """Test that all_subcategories returns a flat list across all categories."""
        config = self._make_config()
        subs = config.all_subcategories()
        assert len(subs) == 3
        assert [s.name for s in subs] == ["trabajo", "educacion", "habilidades"]


@pytest.mark.unit
class TestLoadCategoriesFromYaml:
    """Tests for YAML loading."""

    def test_load_valid_yaml(self, tmp_path):
        """Test loading a valid YAML file into CategoriesConfig."""
        data = {
            "hypothesis_template": "Trata sobre {}.",
            "threshold": 0.6,
            "categories": [
                {
                    "name": "experiencia",
                    "label": "Experiencia",
                    "subcategories": [
                        {"name": "trabajo", "label": "empleo"},
                        {"name": "edu", "label": "educacion", "description": "desc"},
                    ],
                }
            ],
        }
        yaml_path = tmp_path / "cats.yaml"
        yaml_path.write_text(yaml.dump(data))

        config = load_categories_from_yaml(yaml_path)
        assert len(config.categories) == 1
        assert len(config.categories[0].subcategories) == 2
        assert config.threshold == 0.6
        assert config.categories[0].subcategories[1].description == "desc"

    def test_all_subcategories_from_loaded_yaml(self, tmp_path):
        """Test all_subcategories returns correct flat list from YAML-loaded config."""
        data = {
            "categories": [
                {
                    "name": "g1",
                    "label": "G1",
                    "subcategories": [{"name": "a", "label": "A"}],
                },
                {
                    "name": "g2",
                    "label": "G2",
                    "subcategories": [
                        {"name": "b", "label": "B"},
                        {"name": "c", "label": "C"},
                    ],
                },
            ]
        }
        yaml_path = tmp_path / "cats.yaml"
        yaml_path.write_text(yaml.dump(data))
        config = load_categories_from_yaml(yaml_path)
        subs = config.all_subcategories()
        assert [s.name for s in subs] == ["a", "b", "c"]

    def test_load_missing_file(self, tmp_path):
        """Test that FileNotFoundError is raised for a missing YAML file."""
        with pytest.raises(FileNotFoundError):
            load_categories_from_yaml(tmp_path / "missing.yaml")
