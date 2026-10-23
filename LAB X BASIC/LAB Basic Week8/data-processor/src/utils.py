# data-processor/src/utils.py
import logging
import os


def setup_logging(name, level=logging.INFO):
    """Sets up a logger for a specific module (one handler, no duplicate lines)."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:  # Prevent adding multiple handlers if called multiple times
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    logger.propagate = False  # Avoid printing every message twice via the root logger
    return logger


logger = setup_logging("utils")


def ensure_directory_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    if not path:
        return
    try:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Directory ensured: {path}")
    except OSError as e:
        logger.error(f"Error creating directory {path}: {e}")
        raise
