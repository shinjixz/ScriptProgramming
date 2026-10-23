# agentic-data-processor/src/conversion_tasks.py
import json
from .utils import setup_logging

logger = setup_logging(__name__)


class ConversionTasks:
    """Handles conversions between CSV (list of dicts) and JSON formats."""

    def __init__(self):
        logger.info("ConversionTasks initialized.")

    @staticmethod
    def _convert_value(value):
        """Converts a CSV string into int / float / bool / None where possible."""
        if value is None:
            return None
        v = value.strip()
        if v == '' or v.lower() == 'null':
            return None
        if v.lower() in ('true', 'false'):
            return v.lower() == 'true'
        try:
            return int(v)
        except ValueError:
            pass
        try:
            return float(v)
        except ValueError:
            return v

    def csv_to_json(self, csv_data):
        """Converts CSV data (list of dicts of strings) to typed JSON-compatible list of dicts."""
        if not csv_data:
            logger.warning("No CSV data to convert to JSON.")
            return []
        json_data = [{k: self._convert_value(v) for k, v in row.items()} for row in csv_data]
        logger.info(f"Converted {len(csv_data)} CSV rows to JSON format.")
        return json_data

    def json_to_csv(self, json_data, fieldnames=None):
        """Flattens JSON objects (one level of nesting, e.g. details.brand) into CSV rows."""
        if not json_data:
            logger.warning("No JSON data to convert to CSV.")
            return [], []
        if fieldnames is None:
            all_keys = set()
            for item in json_data:
                for k, v in item.items():
                    if isinstance(v, dict):
                        all_keys.update(f"{k}.{sub_k}" for sub_k in v.keys())
                    else:
                        all_keys.add(k)
            fieldnames = sorted(all_keys)
            logger.info(f"Inferred fieldnames for JSON to CSV: {fieldnames}")

        csv_rows = []
        for item in json_data:
            row = {}
            for field in fieldnames:
                if '.' in field:
                    parent, child = field.split('.', 1)
                    nested = item.get(parent)
                    val = nested.get(child, '') if isinstance(nested, dict) else ''
                else:
                    val = item.get(field, '')
                row[field] = json.dumps(val, ensure_ascii=False) if isinstance(val, (dict, list)) else val
            csv_rows.append(row)
        logger.info(f"Converted {len(json_data)} JSON objects to CSV format.")
        return csv_rows, fieldnames
