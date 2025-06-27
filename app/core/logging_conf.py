""" Logger """

from logging import getLogger, StreamHandler, FileHandler, Formatter
from core.config import EXECUTION_LOG_PATH

# pylint: disable=too-few-public-methods

# Define a formatter for log messages with a specific format and date style
_FORMATTER = Formatter(
    fmt="{asctime} - {levelname} - {filename}:{lineno} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class Logging:
    """
    A class to configure and manage logging for the application.

    Attributes:
        __name (str): The name of the logger instance.
    """

    def __init__(self, name):
        """
        Initialize the Logging class with a logger name.

        Args:
            name (str): The name of the logger instance.
        """
        self.__name = name

    def log(self):
        """
        Configure and return a logger instance.

        The logger is set up with both console and file handlers, using the
        predefined formatter. The log level is set to DEBUG.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = getLogger(self.__name)

        # Create a console handler for logging to the terminal
        console_handler = StreamHandler()

        # Create a file handler for logging to a file
        file_handler = FileHandler(EXECUTION_LOG_PATH, mode="a", encoding="utf-8")

        # Set the formatter for both handlers
        file_handler.setFormatter(_FORMATTER)
        console_handler.setFormatter(_FORMATTER)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # Set the logging level to DEBUG
        logger.setLevel(level="DEBUG")

        return logger
