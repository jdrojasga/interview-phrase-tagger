"""Module for transcription-related classes and functions."""

# Core abstractions (what users need)
import iptag.transcriptions.loader.implementations  # noqa: F401
from iptag.transcriptions.loader.base import TranscriptionLoader
from iptag.transcriptions.loader.config import TranscriptionLoaderConfig
from iptag.transcriptions.loader.factory import TranscriptionLoaderFactory

__all__ = [
    # Base classes
    "TranscriptionLoader",
    "TranscriptionLoaderConfig",
    "TranscriptionLoaderFactory",
]
