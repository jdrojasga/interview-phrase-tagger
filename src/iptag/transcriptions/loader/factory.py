"""Factory module to create transcription loader instances based on configuration."""

from typing import Dict

from iptag.transcriptions.loader.base import TranscriptionLoader
from iptag.transcriptions.loader.config import TranscriptionLoaderConfig
from iptag.utils.logging import get_logger


class TranscriptionLoaderFactory:
    """Factory class to create transcription loader instances."""

    _registry: Dict[str, type] = {}
    logger = get_logger(__name__)

    @classmethod
    def register(cls, loader_type: str, loader_cls: type) -> None:
        """Register a new loader class.

        Args:
            loader_type: Unique identifier for the loader type
            loader_cls: Loader class to register

        Raises:
            ValueError: If loader type is already registered
        """
        if loader_type in cls._registry:
            raise ValueError(f"Loader type '{loader_type}' is already registered")
        cls._registry[loader_type] = loader_cls

    @classmethod
    def from_config(cls, config: TranscriptionLoaderConfig) -> TranscriptionLoader:
        """Create a loader instance from configuration.

        Args:
            config: TranscriptionLoaderConfig instance

        Returns:
            TranscriptionLoader instance

        Raises:
            ValueError: If loader type is not registered
        """
        cls.logger.debug(f"Creating loader from config: {config}")
        loader_type = config.type
        if loader_type not in cls._registry:
            raise ValueError(f"Unknown loader type: {loader_type}")
        loader_cls = cls._registry[loader_type]
        return loader_cls(**config.parameters)


# Decorator to register loaders
def register_loader(loader_type: str):
    """Decorator to auto-register loaders."""

    def decorator(cls):
        TranscriptionLoaderFactory.register(loader_type, cls)
        return cls

    return decorator
