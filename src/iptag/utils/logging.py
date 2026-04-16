"""Custom logging module with modified format.

For more information about the python's logging system please
read the docs:
https://docs.python.org/3/library/logging.html
"""

import logging
from typing import Any

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


def get_logger_for(obj: Any, level: int = LOGGING_LEVEL) -> logging.Logger:
    """Get a logger for the given object according to its class and qualname.

    Arguments:
        obj (Any): The object to set the logger to
        level (int): The level to set the logger to.

    Returns:
        logging.Logger: The logger for the object.
    """
    module = obj.__class__.__module__
    qualname = obj.__class__.__qualname__

    return get_logger(f"{module}.{qualname}", level)


class LoggerMixin:
    """Mixin class that provides automatic logger configuration.

    This mixin can be inherited by any class to automatically set up a logger specific
    to that class.
    """

    def __init__(self, *args, **kwargs):  # noqa: D417
        """Initialize the logger."""
        # Call super initialization to support cooperative multiple inheritance
        # This ensures other mixins in the MRO chain get initialized
        super().__init__(*args, **kwargs)
        self.logger = get_logger_for(self)
