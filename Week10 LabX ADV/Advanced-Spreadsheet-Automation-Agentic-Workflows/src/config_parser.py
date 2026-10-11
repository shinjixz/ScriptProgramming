# agentic-spreadsheet-processor/src/config_parser.py
import json
import os

from .utils import setup_logging

logger = setup_logging(__name__)

# Tasks that work on two sheets use source_sheet/dest_sheet instead of "sheet"
TASKS_WITHOUT_SHEET = {"copy_data"}


class ConfigParser:
    """
    Parses and validates the spreadsheet automation configuration from a JSON file.
    """

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        """Loads the configuration from the specified JSON file."""
        if not os.path.exists(self.config_path):
            logger.critical(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            logger.critical(f"Invalid JSON format in config file: {e}")
            raise ValueError(f"Invalid JSON format in config file: {e}")

        self._validate_config()  # raises ValueError with a clear message
        logger.info(f"Configuration loaded successfully from {self.config_path}")
        return self.config

    def _validate_config(self):
        """
        Validates the loaded configuration to ensure required fields and task structures are present.
        This validation can be extended based on all possible task types.
        """
        required_top_level_fields = ["input_file", "output_file", "tasks"]
        for field in required_top_level_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field in config: '{field}'")

        if not isinstance(self.config["tasks"], list):
            raise ValueError("Config field 'tasks' must be a list.")

        # Basic validation for each task
        for i, task in enumerate(self.config["tasks"]):
            if "type" not in task:
                raise ValueError(f"Task {i} is missing 'type' field.")

            if task["type"] in TASKS_WITHOUT_SHEET:
                if "source_sheet" not in task or "dest_sheet" not in task:
                    raise ValueError(f"Task {i} ({task['type']}) requires 'source_sheet' and 'dest_sheet'.")
            elif "sheet" not in task:
                raise ValueError(f"Task {i} is missing 'sheet' field.")

            if task["type"] == "chart":
                if "chart_type" not in task or "data_range" not in task:
                    raise ValueError(f"Chart task {i} requires 'chart_type' and 'data_range'.")

            if task["type"] == "conditional_format":
                if "range" not in task or "rule_type" not in task:
                    raise ValueError(f"Conditional format task {i} requires 'range' and 'rule_type'.")

        logger.info("Configuration validated.")
