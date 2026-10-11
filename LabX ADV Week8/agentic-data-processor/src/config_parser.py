# agentic-data-processor/src/config_parser.py
import json
import os
from .utils import setup_logging

logger = setup_logging(__name__)

# Tasks that produce data and therefore need somewhere to store it
TASKS_REQUIRING_OUTPUT_KEY = [
    "load_csv", "load_json", "transform_csv_aggregate", "filter_csv",
    "update_json_data", "csv_to_json_conversion", "json_to_csv_conversion",
]
# Tasks that consume data from the data store
TASKS_REQUIRING_INPUT_KEY = [
    "save_csv", "save_json", "transform_csv_aggregate", "filter_csv",
    "update_json_data", "query_json_data", "csv_to_json_conversion", "json_to_csv_conversion",
]


class ConfigParser:
    """Parses and validates the data automation configuration from a JSON file."""

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
        self._validate_config()
        logger.info(f"Configuration loaded successfully from {self.config_path}")
        return self.config

    def _validate_config(self):
        """Validates required fields and task structures."""
        if "tasks" not in self.config:
            raise ValueError("Missing required field in config: 'tasks'")
        if not isinstance(self.config["tasks"], list):
            raise ValueError("Config field 'tasks' must be a list.")

        for i, task in enumerate(self.config["tasks"]):
            if "type" not in task:
                raise ValueError(f"Task {i} is missing 'type' field.")
            t = task["type"]
            # FIX: save tasks only write files, so output_data_key is required only for data-producing tasks
            if t in TASKS_REQUIRING_OUTPUT_KEY and "output_data_key" not in task:
                raise ValueError(f"Task {i} (type: {t}) is missing 'output_data_key' field.")
            if t in TASKS_REQUIRING_INPUT_KEY and "input_data_key" not in task:
                raise ValueError(f"Task {i} (type: {t}) requires 'input_data_key'.")
            if t in ["load_csv", "load_json", "save_csv", "save_json"] and "file_path" not in task:
                raise ValueError(f"Task {i} (type: {t}) requires 'file_path'.")
            if t == "save_csv" and "fieldnames" not in task:
                logger.warning(f"Task {i} (save_csv) has no explicit 'fieldnames'. Will derive from data.")
        logger.info("Configuration validated.")
