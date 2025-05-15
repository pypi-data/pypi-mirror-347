import sys
import logging


def log_error_and_exit(logger: logging.Logger, message: str):
    """
    Log an error message and exit with error
    """
    logger.error(message)
    sys.exit(1)
