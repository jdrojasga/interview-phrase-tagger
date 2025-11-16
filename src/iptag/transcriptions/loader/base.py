"""Module for transcription loader base class and registration decorator."""

# define interface using ABC class
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Sequence, Union

from iptag.transcriptions.loader.models import TranscriptionData


class TranscriptionLoader(ABC):
    """Abstract base class for transcription loaders.

    This defines the interface that all concrete loaders must implement.
    Follows Interface Segregation Principle - only essential methods.
    """

    @abstractmethod
    def load(self, source: Union[str, Path], **kwargs) -> TranscriptionData:
        """Load a single transcription from the specified source.

        Args:
            source: Path or identifier to the transcription source
            **kwargs: Additional loader-specific parameters

        Returns:
            TranscriptionData object containing the transcription
        """
        pass

    @abstractmethod
    def load_multiple(
        self, sources: Sequence[Union[str, Path]], **kwargs
    ) -> List[TranscriptionData]:
        """Load multiple transcriptions.

        Args:
            sources: List of paths or identifiers
            **kwargs: Additional loader-specific parameters

        Returns:
            List of TranscriptionData objects
        """
        pass

    @abstractmethod
    def validate_source(self, source: Union[str, Path]) -> bool:
        """Validate if the source can be loaded by this loader.

        Args:
            source: Path or identifier to validate

        Returns:
            True if source is valid for this loader
        """
        pass
