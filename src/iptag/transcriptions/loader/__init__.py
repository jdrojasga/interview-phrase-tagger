"""Module for transcription-related classes and functions."""

# Core abstractions (what users need)
from iptag.transcriptions.loader.base import TranscriptionLoader
from iptag.transcriptions.loader.config import TranscriptionLoaderConfig
from iptag.transcriptions.loader.factory import TranscriptionLoaderFactory
from iptag.transcriptions.loader.implementations import *
from iptag.transcriptions.loader.models import TranscriptionData

__all__ = [
    # Base classes
    "TranscriptionLoader",
    "TranscriptionData",
    "TranscriptionLoaderConfig",
    "TranscriptionLoaderFactory",
]
