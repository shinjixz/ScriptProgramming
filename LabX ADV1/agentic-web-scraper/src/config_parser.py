# agentic-web-scraper/src/config_parser.py
import json
import os


class ConfigParser:
    """Parses and validates the scraping configuration from a JSON file."""

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        """Loads the configuration from the specified JSON file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in config file: {e}")
        self._validate_config()
        return self.config

    def _validate_config(self):
        """Validates that the required fields are present and well-typed."""
        required_fields = [
            "start_url",
            "pagination_selector",
            "item_container_selector",
            "item_data_selectors",
        ]
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field in config: '{field}'")

        for field in ["name", "price"]:  # Minimum fields for a product
            if not self.config["item_data_selectors"].get(field):
                raise ValueError(f"Missing required item data selector: '{field}'")

        # Selectors must be strings; null means "this field is not on the page"
        for key, value in self.config["item_data_selectors"].items():
            if value is not None and not isinstance(value, str):
                raise ValueError(f"Item data selector '{key}' must be a string or null.")

        if not isinstance(self.config["pagination_selector"], (str, type(None))):
            raise ValueError("Pagination selector must be a string or null.")
        if not isinstance(self.config["item_container_selector"], str):
            raise ValueError("Item container selector must be a string.")
