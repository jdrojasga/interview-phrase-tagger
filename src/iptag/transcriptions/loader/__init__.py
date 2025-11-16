"""Module for transcription-related classes and functions."""

# Core abstractions (what users need)
from iptag.transcriptions.loader.base import TranscriptionLoader
from iptag.transcriptions.loader.config import TranscriptionLoaderConfig
from iptag.transcriptions.loader.factory import TranscriptionLoaderFactory
from iptag.transcriptions.loader.implementations import *

__all__ = [
    # Base classes
    "TranscriptionLoader",
    "TranscriptionLoaderConfig",
    "TranscriptionLoaderFactory",
]
