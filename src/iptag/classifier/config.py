"""Configuration models for the classifier module."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class SubcategoryDefinition(BaseModel):
    """Definition of a single classification subcategory (classifier label)."""

    name: str
    label: str
    description: Optional[str] = None


class CategoryDefinition(BaseModel):
    """A named group of subcategories."""

    name: str
    label: str
    description: Optional[str] = None
    subcategories: list[SubcategoryDefinition]


class CategoriesConfig(BaseModel):
    """Configuration for classification categories."""

    categories: list[CategoryDefinition]
    hypothesis_template: str = "Este texto trata sobre {}."
    threshold: float = 0.5

    def all_subcategories(self) -> list[SubcategoryDefinition]:
        """Flat list of all subcategories across all categories, in order."""
        return [sub for cat in self.categories for sub in cat.subcategories]


def load_categories_from_yaml(path: Path) -> CategoriesConfig:
    """Load categories configuration from a YAML file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        CategoriesConfig instance.

    Raises:
        FileNotFoundError: If the YAML file does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Categories config not found: {path}")
    with open(path) as f:
        data = yaml.safe_load(f)
    return CategoriesConfig(**data)
