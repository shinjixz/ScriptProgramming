# agentic-data-processor/main.py
import os
import sys

# FIX: import 'src' as a package (the modules use relative imports like `from .utils import ...`,
# so adding src/ to sys.path and importing `config_parser` directly raises ImportError)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.config_parser import ConfigParser
from src.data_agent import DataAgent
from src.utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


def check_required_input_files(config):
    """Checks that every input file for load_* tasks exists before the agent starts."""
    ok = True
    for task in config['tasks']:
        if task['type'] in ['load_csv', 'load_json'] and not os.path.exists(task['file_path']):
            logger.critical(f"Required input file '{task['file_path']}' not found for task '{task.get('name')}'.")
            ok = False
    return ok


def main():
    config_file_path = os.path.join(BASE_DIR, 'configs', 'data_pipeline_config.json')
    try:
        for folder in ('data', 'configs', 'reports'):
            ensure_directory_exists(os.path.join(BASE_DIR, folder))

        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        # Make file paths in the config relative to the project root
        for task in config['tasks']:
            if 'file_path' in task:
                task['file_path'] = os.path.join(BASE_DIR, task['file_path'])

        if not check_required_input_files(config):
            logger.critical("One or more required input files are missing. See README.md.")
            return

        agent = DataAgent(config, base_dir=BASE_DIR)
        report = agent.run()
        logger.info(f"Data automation process completed. Audit report: {report}")
    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
