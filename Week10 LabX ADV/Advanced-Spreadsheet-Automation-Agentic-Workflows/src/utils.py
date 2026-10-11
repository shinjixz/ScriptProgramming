# agentic-spreadsheet-processor/src/utils.py
import logging
import json
import os


def setup_logging(name, level=logging.INFO, filename=None):
    """Sets up a logger for specific modules."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicate lines via the root logger
    if not logger.handlers:  # Prevent adding multiple handlers if called multiple times
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        # File handler (optional)
        if filename:
            fh = logging.FileHandler(filename, encoding='utf-8')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    return logger


_logger = setup_logging(__name__)


def save_json_report(data, filename, directory='data'):
    """Saves a dictionary or list to a JSON file."""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        _logger.info(f"Report saved to {filepath}")
        return True
    except IOError as e:
        _logger.error(f"Error saving report to JSON file: {e}")
        return False
