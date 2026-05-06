"""Zero-shot NLI classifier for multilabel text classification."""

from typing import Optional

from transformers import pipeline

from iptag.classifier.catalog import resolve_model
from iptag.classifier.config import CategoriesConfig
from iptag.classifier.models import ClassificationResult
from iptag.settings import IptagSettings
from iptag.utils.logging import LoggerMixin


class ZeroShotClassifier(LoggerMixin):
    """Zero-shot multilabel classifier using HuggingFace NLI models.

    Uses the zero-shot-classification pipeline to classify text segments
    against a set of candidate labels without any training data.
    """

    def __init__(
        self,
        model_name_or_path: Optional[str] = None,
        device: str = "cpu",
        batch_size: int = 8,
    ):
        """Initialize the classifier.

        Args:
            model_name_or_path: Catalog alias ('fast', 'balanced', 'accurate'),
                HuggingFace model ID, or None to read from CLASSIFIER_MODEL env var.
            device: Device for inference ('cpu' or 'cuda').
            batch_size: Batch size for classify_batch.
        """
        super().__init__()
        alias_or_id = model_name_or_path or IptagSettings().classifier_model
        self.model_name_or_path = resolve_model(alias_or_id)
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
        subcategories = categories.all_subcategories()
        candidate_labels = [sub.description or sub.label for sub in subcategories]

        result = pipe(
            text,
            candidate_labels,
            hypothesis_template=categories.hypothesis_template,
            multi_label=True,
        )

        candidate_to_name = {
            (sub.description or sub.label): sub.name for sub in subcategories
        }
        scores = {
            candidate_to_name[label]: score
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
