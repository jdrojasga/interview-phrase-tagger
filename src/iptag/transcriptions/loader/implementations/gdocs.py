"""Module for Google Docs transcription loader implementation."""

# define interface using ABC class
from pathlib import Path
from typing import List, Optional, Sequence, Union

from iptag.transcriptions.loader.base import (
    TranscriptionData,
    TranscriptionLoader,
)
from iptag.transcriptions.loader.factory import register_loader


@register_loader("gdocs")
class GDocsTranscriptionLoader(TranscriptionLoader):
    """Loader for Google Docs transcriptions.

    Note: Requires google-auth and google-api-python-client packages.
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize Google Docs loader.

        Args:
            credentials_path: Path to Google API credentials JSON
        """
        self.credentials_path = credentials_path
        self._service = None

    def _get_service(self):
        """Lazy initialization of Google Docs API service."""
        if self._service is None:
            # This is a placeholder - actual implementation would use Google API
            raise NotImplementedError(
                "Google Docs loader requires google-auth and google-api-python-client. "
                "Install with: pip install google-auth google-api-python-client"
            )
        return self._service

    def load(self, source: Union[str, Path], **kwargs) -> TranscriptionData:
        """Load transcription from a Google Doc.

        Args:
            source: Google Doc ID or URL
            **kwargs: Additional loader-specific parameters

        Returns:
            TranscriptionData object
        """
        # Extract doc ID from URL if needed
        doc_id = self._extract_doc_id(str(source))

        # Placeholder implementation
        # Real implementation would use:
        # service = self._get_service()
        # document = service.documents().get(documentId=doc_id).execute()
        # text = self._extract_text_from_doc(document)

        raise NotImplementedError("Google Docs loader not fully implemented yet")

    def load_multiple(
        self, sources: Sequence[Union[str, Path]], **kwargs
    ) -> List[TranscriptionData]:
        """Load multiple Google Docs."""
        return [self.load(source, **kwargs) for source in sources]

    def validate_source(self, source: Union[str, Path]) -> bool:
        """Validate Google Docs source."""
        source_str = str(source)
        # Check if it's a Google Docs URL or ID
        return "docs.google.com" in source_str or len(source_str) == 44

    def _extract_doc_id(self, source: str) -> str:
        """Extract document ID from URL or return as-is if already an ID."""
        if "docs.google.com" in source:
            # Extract ID from URL
            parts = source.split("/")
            for i, part in enumerate(parts):
                if part == "d" and i + 1 < len(parts):
                    return parts[i + 1]
        return source
