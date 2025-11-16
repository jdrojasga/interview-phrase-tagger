"""Module for transcription data models."""

from typing import Any, Dict, Optional


class TranscriptionData:
    """Data class to hold transcription information."""

    def __init__(
        self,
        text: str,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Initialize transcription data.

        Args:
            text: The transcription text content
            source: Source identifier (filename, URL, etc.)
            metadata: Optional metadata (e.g., timestamp, speaker info)
        """
        self.text = text
        self.source = source
        self.metadata = metadata or {}

    def __repr__(self) -> str:
        """String representation."""
        return f"TranscriptionData(source={self.source}, length={len(self.text)})"
