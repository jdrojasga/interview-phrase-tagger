"""Custom logging module with modified format.

For more information about the python's logging system please
read the docs:
https://docs.python.org/3/library/logging.html
"""

import logging

from iptag.settings import IptagSettings

# Export the levels
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


def get_logging_level() -> int:
    """Get the logging level based on settings."""
    return DEBUG if IptagSettings().debug else INFO


# Define the format as we want the logs
LOGGING_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOGGING_LEVEL = get_logging_level()
logging.basicConfig(format=LOGGING_FORMAT, level=LOGGING_LEVEL)


def get_logger(name: str, level: int = LOGGING_LEVEL) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name (str): Name of the logger.
        level (int): Logging level for the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


class LoggerMixin:
    """Mixin class that provides automatic logger configuration."""

    @property
    def logger(self) -> logging.Logger:
        """Get a logger instance named after the concrete class."""
        if not hasattr(self, "_logger"):
            self._logger = get_logger(
                f"{self.__class__.__module__}.{self.__class__.__name__}"
            )
        return self._logger
