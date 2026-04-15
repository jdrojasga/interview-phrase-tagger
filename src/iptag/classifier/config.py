"""Configuration models for the classifier module."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class CategoryDefinition(BaseModel):
    """Definition of a single classification category."""

    name: str
    label: str
    description: Optional[str] = None


class CategoriesConfig(BaseModel):
    """Configuration for classification categories."""

    categories: list[CategoryDefinition]
    hypothesis_template: str = "Este texto trata sobre {}."
    threshold: float = 0.5


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
