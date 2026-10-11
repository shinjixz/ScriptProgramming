# document-automator/src/utils.py
import logging
import os


def setup_logging(name, level=logging.INFO):
    """Sets up a logger for specific modules."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:  # Prevent adding multiple handlers if called multiple times
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False  # Avoid duplicate lines via the root logger
    return logger


_logger = setup_logging(__name__)


def ensure_directory_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    try:
        os.makedirs(path, exist_ok=True)
        _logger.info(f"Directory ensured: {path}")
    except OSError as e:
        _logger.error(f"Error creating directory {path}: {e}")
        raise
