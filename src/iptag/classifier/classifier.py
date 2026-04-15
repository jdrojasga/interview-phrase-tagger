"""Zero-shot NLI classifier for multilabel text classification."""

from typing import Optional

from transformers import pipeline

from iptag.classifier.config import CategoriesConfig
from iptag.classifier.models import ClassificationResult
from iptag.utils.logging import LoggerMixin


class ZeroShotClassifier(LoggerMixin):
    """Zero-shot multilabel classifier using HuggingFace NLI models.

    Uses the zero-shot-classification pipeline to classify text segments
    against a set of candidate labels without any training data.
    """

    DEFAULT_MODEL = "Recognai/zeroshot_selectra_medium"

    def __init__(
        self,
        model_name_or_path: str = DEFAULT_MODEL,
        device: str = "cpu",
        batch_size: int = 8,
    ):
        """Initialize the classifier.

        Args:
            model_name_or_path: HuggingFace model ID or local path.
            device: Device for inference ('cpu' or 'cuda').
            batch_size: Batch size for classify_batch.
        """
        super().__init__()
        self.model_name_or_path = model_name_or_path
        self.device = device
        self.batch_size = batch_size
        self._pipeline: Optional[pipeline] = None

    def _get_pipeline(self):
        """Lazy-load the classification pipeline."""
        if self._pipeline is None:
            self.logger.info(
                f"Loading model '{self.model_name_or_path}' on {self.device}..."
            )
            self._pipeline = pipeline(
                "zero-shot-classification",
                model=self.model_name_or_path,
                device=self.device,
            )
            self.logger.info("Model loaded successfully.")
        return self._pipeline

    def classify(
        self,
        text: str,
        categories: CategoriesConfig,
        index: int = 0,
    ) -> ClassificationResult:
        """Classify a single text against the given categories.

        Args:
            text: Text to classify.
            categories: Categories configuration with labels and threshold.
            index: Position index of this text in a sequence.

        Returns:
            ClassificationResult with assigned labels and scores.
        """
        pipe = self._get_pipeline()
        candidate_labels = [cat.label for cat in categories.categories]

        result = pipe(
            text,
            candidate_labels,
            hypothesis_template=categories.hypothesis_template,
            multi_label=True,
        )

        label_to_name = {cat.label: cat.name for cat in categories.categories}
        scores = {
            label_to_name[label]: score
            for label, score in zip(result["labels"], result["scores"])
        }
        assigned = [
            name for name, score in scores.items() if score >= categories.threshold
        ]

        return ClassificationResult(
            text=text,
            labels=assigned,
            scores=scores,
            index=index,
        )

    def classify_batch(
        self,
        texts: list[str],
        categories: CategoriesConfig,
    ) -> list[ClassificationResult]:
        """Classify a batch of texts against the given categories.

        Args:
            texts: List of texts to classify.
            categories: Categories configuration with labels and threshold.

        Returns:
            List of ClassificationResult objects.
        """
        self.logger.debug(f"Classifying batch of {len(texts)} texts.")
        results = []
        for i, text in enumerate(texts):
            result = self.classify(text, categories, index=i)
            results.append(result)
        return results
