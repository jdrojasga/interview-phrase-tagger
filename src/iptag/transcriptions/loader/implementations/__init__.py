"""Module for transcription loader implementations."""

from iptag.transcriptions.loader.implementations.gdocs import GDocsTranscriptionLoader
from iptag.transcriptions.loader.implementations.txt import TxtTranscriptionLoader

__all__ = [
    "GDocsTranscriptionLoader",
    "TxtTranscriptionLoader",
]
