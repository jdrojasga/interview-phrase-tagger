"""Module for transcription data models."""

from typing import Any, Dict, Optional


class TranscriptionData:
    """Data class to hold transcription information."""

    def __init__(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
    ):
        """Initialize transcription data.

        Args:
            text: The transcription text content
            metadata: Optional metadata (e.g., timestamp, speaker info)
            source: Source identifier (filename, URL, etc.)
        """
        self.text = text
        self.metadata = metadata or {}
        self.source = source

    def __repr__(self) -> str:
        """String representation."""
        return f"TranscriptionData(source={self.source}, length={len(self.text)})"
