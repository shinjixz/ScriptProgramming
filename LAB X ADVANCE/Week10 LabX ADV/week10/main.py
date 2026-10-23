# agentic-spreadsheet-processor/main.py
import os
import sys

from src.config_parser import ConfigParser
from src.spreadsheet_agent import SpreadsheetAgent
from src.utils import setup_logging

logger = setup_logging("main")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    """
    Main entry point for the Agentic Spreadsheet Processor.
    Loads config and runs the agent.
    Usage: python main.py [path/to/config.json]
    """
    # Run relative to the project folder so "data/..." paths in the config always resolve
    os.chdir(BASE_DIR)
    config_file_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        "configs", "example_spreadsheet_config.json")

    try:
        os.makedirs("data", exist_ok=True)
        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        input_file_path = config.get("input_file")
        if not os.path.exists(input_file_path):
            logger.critical(f"Input Excel file not found: '{input_file_path}'. "
                            f"Run 'python create_input_data.py' first.")
            return 1

        logger.info("Initializing Spreadsheet Agent...")
        agent = SpreadsheetAgent(config)
        logger.info("Running Spreadsheet Agent...")
        return 0 if agent.run() else 1

    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
        logger.info("Please check the format and required fields in your config file.")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred during execution: {e}", exc_info=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
