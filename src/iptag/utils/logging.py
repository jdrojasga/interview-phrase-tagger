"""Custom logging module with modified format.

For more information about the python's logging system please
read the docs:
https://docs.python.org/3/library/logging.html
"""

import logging

# Define the format as we want the logs
LOGGING_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT)

# Export the levels
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


def get_logger(name: str, level: int = INFO) -> logging.Logger:
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
