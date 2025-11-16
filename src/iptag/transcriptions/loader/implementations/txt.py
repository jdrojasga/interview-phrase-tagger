"""Module for plain text transcription loader implementation."""

# define interface using ABC class
from pathlib import Path
from typing import List, Sequence, Union

from iptag.transcriptions.loader.base import (
    TranscriptionData,
    TranscriptionLoader,
)
from iptag.transcriptions.loader.factory import register_loader


@register_loader("txt")
class TxtTranscriptionLoader(TranscriptionLoader):
    """Loader for plain text transcription files."""

    def __init__(self, encoding: str = "utf-8", strip_whitespace: bool = True):
        """Initialize TXT loader.

        Args:
            encoding: Text encoding to use
            strip_whitespace: Whether to strip leading/trailing whitespace
        """
        self.encoding = encoding
        self.strip_whitespace = strip_whitespace

    def load(self, source: Union[str, Path], **kwargs) -> TranscriptionData:
        """Load transcription from a text file."""
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")

        with open(path, "r", encoding=self.encoding) as f:
            text = f.read()

        if self.strip_whitespace:
            text = text.strip()

        metadata = {
            "file_size": path.stat().st_size,
            "file_name": path.name,
            "encoding": self.encoding,
        }

        return TranscriptionData(text=text, metadata=metadata, source=str(source))

    def load_multiple(
        self, sources: Sequence[Union[str, Path]], **kwargs
    ) -> List[TranscriptionData]:
        """Load multiple text files."""
        return [self.load(source, **kwargs) for source in sources]

    def validate_source(self, source: Union[str, Path]) -> bool:
        """Validate text file source."""
        path = Path(source)
        return path.exists() and path.suffix.lower() in [".txt", ".text"]
