"""Example script demonstrating the full classification pipeline."""

from pathlib import Path

from iptag.classifier import (
    ZeroShotClassifier,
    classify_transcription,
    load_categories_from_yaml,
)
from iptag.transcriptions.loader import (
    TranscriptionLoaderConfig,
    TranscriptionLoaderFactory,
)
from iptag.transcriptions.splitter.text import split_text_using_regex


def main() -> None:
    """Run end-to-end classification on a sample transcription."""
    # 1. Load transcription
    config = TranscriptionLoaderConfig(type="txt", parameters={"encoding": "utf-8"})
    loader = TranscriptionLoaderFactory.from_config(config)

    data_path = Path("data/raw")
    transcription = loader.load(data_path / "transcription1.txt")
    print(f"Loaded: {transcription}")

    # 2. Split into sentences
    split_text_using_regex(transcription, regex=r"[.!?]+\s+")
    sentences = transcription.metadata["sentences"]
    print(f"Sentences ({len(sentences)}):")
    for i, s in enumerate(sentences):
        print(f"  [{i}] {s}")

    # 3. Load categories
    categories = load_categories_from_yaml(Path("configs/topics_example.yaml"))
    print(f"\nCategories: {[c.name for c in categories.categories]}")

    # 4. Classify
    classifier = ZeroShotClassifier()
    classify_transcription(transcription, classifier, categories)

    # 5. Print results
    print("\n--- Classification Results ---")
    for result in transcription.metadata["classifications"]:
        assigned = ", ".join(result.labels) if result.labels else "(none)"
        print(f"[{assigned}] {result.text}")
        for name, score in sorted(result.scores.items(), key=lambda x: -x[1]):
            print(f"    {name}: {score:.3f}")


if __name__ == "__main__":
    main()
