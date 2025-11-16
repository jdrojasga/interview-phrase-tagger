"""Script to load transcription data from various sources."""

from pathlib import Path
from typing import List, Sequence, Union

from iptag.transcriptions.loader import (
    TranscriptionData,
    TranscriptionLoaderConfig,
    TranscriptionLoaderFactory,
)


def load_transcriptions(
    source_type: str, sources: Sequence[Union[str, Path]], **loader_kwargs
) -> List[TranscriptionData]:
    """Load transcriptions using the specified loader type.

    Args:
        source_type: Type of the transcription source (e.g., 'txt')
        sources: List of paths or identifiers to load
        **loader_kwargs: Additional parameters for the loader

    Returns:
        List of TranscriptionData objects
    """
    config = TranscriptionLoaderConfig(type=source_type, parameters=loader_kwargs)
    loader = TranscriptionLoaderFactory.from_config(config)
    return loader.load_multiple(sources)


if __name__ == "__main__":
    # Example usage
    data_path = Path("data/raw")
    sources = [data_path / "transcription1.txt", data_path / "transcription2.txt"]
    transcriptions = load_transcriptions("txt", sources, encoding="utf-8")
    for transcription in transcriptions:
        print(transcription)
        print(transcription.text[:40])
