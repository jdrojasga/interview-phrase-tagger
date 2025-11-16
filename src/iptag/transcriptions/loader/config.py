"""Configuration module for transcription loaders."""

from typing import Any, Dict

from pydantic import BaseModel


class TranscriptionLoaderConfig(BaseModel):
    """Configuration class for transcription loaders.

    Attributes:
        type (str): Type of the loader (e.g., 'txt', 'csv', 'gdocs')
        parameters (Dict[str, Any]): Loader-specific parameters
    """

    type: str
    parameters: Dict[str, Any] = {}
