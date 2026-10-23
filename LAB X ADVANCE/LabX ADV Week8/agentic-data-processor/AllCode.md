# AllCode — Agentic Data Processor (fixed version)

## 1. `src/__init__.py`

```python
# package marker
```

## 2. `src/utils.py`

```python
# agentic-data-processor/src/utils.py
import logging
import os
import json
import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_logging(name, level=logging.INFO, log_file=None):
    """Sets up a logger for specific modules, allowing file output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Ensure handlers are added only once per logger instance
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        # Prevent duplicate lines via the root logger configured by basicConfig
        logger.propagate = False
    return logger


def ensure_directory_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    if not path:
        return
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Error creating directory {path}: {e}")
        raise


def log_audit_entry(audit_log_list, status, message, task_type="N/A", details=None):
    """Adds an entry to the audit log list."""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": status,
        "task_type": task_type,
        "message": message,
        "details": details if details else {}
    }
    audit_log_list.append(log_entry)
    if status in ("ERROR", "CRITICAL"):
        logging.error(f"AUDIT LOG - {status}: {message} | Task: {task_type} | Details: {details}")
    else:
        logging.info(f"AUDIT LOG - {status}: {message} | Task: {task_type}")
```

## 3. `src/config_parser.py`

```python
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
```

## 4. `src/csv_tasks.py`

```python
# agentic-data-processor/src/csv_tasks.py
import csv
import os
from collections import defaultdict
from .utils import setup_logging, ensure_directory_exists  # FIX: ensure_directory_exists was not imported

logger = setup_logging(__name__)


class CSVTasks:
    """Handles advanced reading, writing, and processing of CSV files (as lists of dicts)."""

    def __init__(self):
        logger.info("CSVTasks initialized.")

    def load_csv(self, file_path):
        """Loads a CSV file and returns its content as a list of dictionaries."""
        if not os.path.exists(file_path):
            logger.error(f"CSV file not found: {file_path}")
            return None
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                data = list(csv.DictReader(file))
            logger.info(f"Successfully loaded {len(data)} rows from '{file_path}'.")
            return data
        except Exception as e:
            logger.error(f"Error loading CSV file '{file_path}': {e}")
            return None

    def save_csv(self, data, file_path, fieldnames=None):
        """Saves a list of dictionaries to a CSV file."""
        if not data:
            logger.warning("No data provided to save to CSV.")
            return False
        ensure_directory_exists(os.path.dirname(file_path))
        if fieldnames is None:
            if isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
                logger.info(f"Inferred fieldnames for CSV: {fieldnames}")
            else:
                logger.error("Cannot infer fieldnames: data is not a list of dictionaries.")
                return False
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Successfully saved {len(data)} rows to '{file_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error saving CSV file '{file_path}': {e}")
            return False

    def transform_csv_aggregate(self, data, group_by_field, aggregate_field, aggregate_type="sum"):
        """Aggregates data by a field. Supports 'sum', 'count', 'average'."""
        if not data:
            logger.warning("No data to aggregate.")
            return []
        aggregated = defaultdict(lambda: {'_count': 0, '_sum': 0.0})
        for row in data:
            group_value = row.get(group_by_field)
            if group_value is None:
                logger.warning(f"Skipping row due to missing group_by_field '{group_by_field}': {row}")
                continue
            try:
                numeric_value = float(row.get(aggregate_field, 0))
                aggregated[group_value]['_sum'] += numeric_value
                aggregated[group_value]['_count'] += 1
            except (ValueError, TypeError) as e:
                logger.warning(f"Skipping row with non-numeric '{aggregate_field}': {row}. Error: {e}")

        results = []
        for group_value, m in aggregated.items():
            result_row = {group_by_field: group_value}
            if aggregate_type == "sum":
                result_row[f'Total_{aggregate_field}'] = round(m['_sum'], 2)
            elif aggregate_type == "count":
                result_row[f'Count_{aggregate_field}'] = m['_count']
            elif aggregate_type == "average":
                result_row[f'Average_{aggregate_field}'] = round(m['_sum'] / m['_count'], 2) if m['_count'] else 0.0
            else:
                logger.warning(f"Unsupported aggregation type: {aggregate_type}.")
                continue
            results.append(result_row)
        logger.info(f"Aggregated data by '{group_by_field}' using '{aggregate_type}'. Produced {len(results)} rows.")
        return results

    def filter_csv(self, data, filter_field, operator, value):
        """Filters data. operator: '>', '<', '>=', '<=', '==', '!='."""
        if not data:
            logger.warning("No data to filter.")
            return []
        ops = {
            '>': lambda a, b: a > b, '<': lambda a, b: a < b,
            '>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b,
            '==': lambda a, b: a == b, '!=': lambda a, b: a != b,
        }
        if operator not in ops:
            logger.warning(f"Unsupported filter operator: '{operator}'.")
            return []
        filtered = []
        for row in data:
            field_value = row.get(filter_field)
            if field_value is None:
                continue
            try:
                compare_value = float(field_value) if isinstance(value, (int, float)) else str(field_value)
                if ops[operator](compare_value, value):
                    filtered.append(row)
            except ValueError as e:
                logger.warning(f"Type conversion error during filter for row: {row}. Error: {e}")
        logger.info(f"Filtered data by '{filter_field} {operator} {value}'. Resulted in {len(filtered)} rows.")
        return filtered
```

## 5. `src/json_tasks.py`

```python
# agentic-data-processor/src/json_tasks.py
import json
import os
from .utils import setup_logging, ensure_directory_exists  # FIX: ensure_directory_exists was not imported

logger = setup_logging(__name__)


class JSONTasks:
    """Handles advanced reading, writing, and manipulation of JSON data."""

    def __init__(self):
        logger.info("JSONTasks initialized.")

    def load_json(self, file_path):
        """Loads a JSON file and returns the Python object."""
        if not os.path.exists(file_path):
            logger.error(f"JSON file not found: {file_path}")
            return None
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"Successfully loaded JSON from '{file_path}'.")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in '{file_path}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading JSON file '{file_path}': {e}")
            return None

    def save_json(self, data, file_path, indent=2):
        """Saves a Python object to a JSON file, with pretty-printing."""
        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            logger.info(f"Successfully saved JSON to '{file_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON file '{file_path}': {e}")
            return False

    @staticmethod
    def _step(node, key):
        """
        Moves one level down the JSON tree.
        - dict  -> node[key]
        - list + numeric key -> node[int(key)]
        - list + non-numeric key -> the item whose "id" equals key (e.g. "PROD001")
        Returns (found, child).
        """
        if isinstance(node, dict):
            return (key in node), node.get(key)
        if isinstance(node, list):
            if key.isdigit():
                idx = int(key)
                return (0 <= idx < len(node)), (node[idx] if 0 <= idx < len(node) else None)
            for item in node:  # NEW: lookup by id inside a list of objects
                if isinstance(item, dict) and str(item.get("id")) == key:
                    return True, item
        return False, None

    def update_json_data(self, data, updates):
        """
        Applies updates to a JSON-like object.
        updates: [{"path": "0.stock", "value": 75, "operation": "set"}, ...]
        operation: 'set' | 'add_to_list' | 'remove_from_list'
        An empty path ("") refers to the root object (e.g. append to the root list).
        """
        if not data:
            logger.warning("No JSON data provided for update.")
            return data
        modified = json.loads(json.dumps(data))  # deep copy

        for update in updates or []:
            path = update.get("path")
            value = update.get("value")
            operation = update.get("operation", "set")
            if path is None:
                logger.warning(f"Update skipped: missing 'path': {update}")
                continue
            try:
                # FIX: empty path = root. Original code skipped it, so PROD004 was never added.
                if path == "":
                    if operation == "add_to_list" and isinstance(modified, list):
                        modified.append(value)
                        logger.info(f"Added item to root list: {value.get('id', value) if isinstance(value, dict) else value}")
                    elif operation == "remove_from_list" and isinstance(modified, list) and value in modified:
                        modified.remove(value)
                        logger.info("Removed item from root list.")
                    else:
                        logger.warning(f"Unsupported root operation '{operation}'. Skipping: {update}")
                    continue

                keys = path.split('.')
                parent = modified
                found = True
                for key in keys[:-1]:
                    found, parent = self._step(parent, key)
                    if not found:
                        logger.warning(f"Path '{path}' not found at key '{key}'. Skipping update.")
                        break
                if not found:
                    continue

                target = keys[-1]
                if operation == "set":
                    if isinstance(parent, dict):
                        parent[target] = value
                        logger.info(f"Set '{path}' to '{value}'.")
                    elif isinstance(parent, list) and target.isdigit() and 0 <= int(target) < len(parent):
                        parent[int(target)] = value
                        logger.info(f"Set '{path}' (list index) to '{value}'.")
                    else:
                        logger.warning(f"Cannot 'set' at path '{path}'. Skipping.")
                elif operation in ("add_to_list", "remove_from_list"):
                    found, lst = self._step(parent, target)
                    if not (found and isinstance(lst, list)):
                        logger.warning(f"Cannot '{operation}' at '{path}': target is not a list.")
                    elif operation == "add_to_list":
                        lst.append(value)
                        logger.info(f"Added '{value}' to list at '{path}'.")
                    elif value in lst:
                        lst.remove(value)
                        logger.info(f"Removed '{value}' from list at '{path}'.")
                    else:
                        logger.warning(f"Value '{value}' not found in list at '{path}'.")
                else:
                    logger.warning(f"Unsupported operation '{operation}' for path '{path}'.")
            except Exception as e:
                logger.error(f"Error applying JSON update for path '{path}': {e}. Update: {update}")
        return modified

    def query_json_data(self, data, path):
        """Queries a value from nested JSON using a dot-notation path. Returns None if not found."""
        if not data:
            logger.warning("No JSON data to query.")
            return None
        node = data
        for key in path.split('.'):
            found, node = self._step(node, key)
            if not found:
                logger.warning(f"Query path '{path}' failed at key '{key}'.")
                return None
        logger.info(f"Successfully queried '{path}'. Result: {node}")
        return node
```

## 6. `src/conversion_tasks.py`

```python
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
```

## 7. `src/data_agent.py`

```python
# agentic-data-processor/src/data_agent.py
import os
import json
import datetime
from .utils import setup_logging, log_audit_entry, ensure_directory_exists
from .csv_tasks import CSVTasks
from .json_tasks import JSONTasks
from .conversion_tasks import ConversionTasks

logger = setup_logging(__name__)


class DataAgent:
    """
    An agent that processes CSV/JSON data based on a structured configuration,
    passing intermediate results between tasks through an internal data_store.
    """

    def __init__(self, config, base_dir=None):
        self.config = config
        # FIX: original used sys.modules['__main__'] without importing sys -> NameError
        self.base_dir = base_dir or os.getcwd()
        self.audit_log = []
        self.data_store = {}
        self.start_time = datetime.datetime.now()
        self.csv_tasks = CSVTasks()
        self.json_tasks = JSONTasks()
        self.conversion_tasks = ConversionTasks()
        # Task dispatcher: maps task "type" -> handler method
        self.handlers = {
            "load_csv": self._handle_load_csv,
            "save_csv": self._handle_save_csv,
            "transform_csv_aggregate": self._handle_aggregate,
            "filter_csv": self._handle_filter,
            "load_json": self._handle_load_json,
            "save_json": self._handle_save_json,
            "update_json_data": self._handle_update_json,
            "query_json_data": self._handle_query_json,
            "csv_to_json_conversion": self._handle_csv_to_json,
            "json_to_csv_conversion": self._handle_json_to_csv,
        }
        logger.info("Data Agent initialized with configuration.")

    # ---------- data store ----------
    def _get_data_from_store(self, key):
        if key not in self.data_store:
            logger.error(f"Data key '{key}' not found in agent's data store.")
            return None
        return self.data_store[key]

    def _set_data_in_store(self, key, data):
        self.data_store[key] = data
        logger.debug(f"Data stored under key: '{key}'.")

    # ---------- handlers: each returns (success, output_data) ----------
    def _handle_load_csv(self, task, data):
        out = self.csv_tasks.load_csv(task["file_path"])
        return out is not None, out

    def _handle_save_csv(self, task, data):
        return self.csv_tasks.save_csv(data, task["file_path"], task.get("fieldnames")), None

    def _handle_aggregate(self, task, data):
        out = self.csv_tasks.transform_csv_aggregate(
            data, task.get("group_by_field"), task.get("aggregate_field"), task.get("aggregate_type", "sum"))
        return out is not None, out

    def _handle_filter(self, task, data):
        out = self.csv_tasks.filter_csv(data, task.get("filter_field"), task.get("operator"), task.get("value"))
        return out is not None, out

    def _handle_load_json(self, task, data):
        out = self.json_tasks.load_json(task["file_path"])
        return out is not None, out

    def _handle_save_json(self, task, data):
        return self.json_tasks.save_json(data, task["file_path"], task.get("indent", 2)), None

    def _handle_update_json(self, task, data):
        out = self.json_tasks.update_json_data(data, task.get("updates", []))
        return out is not None, out

    def _handle_query_json(self, task, data):
        path = task.get("path")
        result = self.json_tasks.query_json_data(data, path)
        log_audit_entry(self.audit_log, "INFO", f"Query result for path '{path}': {result}",
                        task["type"], {"query_path": path, "result": result})
        return True, result

    def _handle_csv_to_json(self, task, data):
        out = self.conversion_tasks.csv_to_json(data)
        return out is not None, out

    def _handle_json_to_csv(self, task, data):
        rows, fieldnames = self.conversion_tasks.json_to_csv(data, task.get("fieldnames"))
        # Keep inferred fieldnames so a following save_csv can reuse them
        if task.get("output_data_key"):
            self._set_data_in_store(task["output_data_key"] + "_fieldnames", fieldnames)
        return rows is not None, rows

    # ---------- dispatcher ----------
    def _process_task(self, task):
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        input_key = task.get("input_data_key")
        output_key = task.get("output_data_key")

        logger.info(f"Executing task: '{task_name}' (Type: {task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type, task)

        handler = self.handlers.get(task_type)
        if handler is None:
            log_audit_entry(self.audit_log, "WARNING", f"Unsupported task type: {task_type}", task_type, task)
            return

        current_data = None
        if input_key:
            current_data = self._get_data_from_store(input_key)
            if current_data is None:
                log_audit_entry(self.audit_log, "ERROR",
                                f"Task '{task_name}' failed: input data '{input_key}' not found in store.",
                                task_type, task)
                return
        try:
            success, output = handler(task, current_data)
            if success and output is not None and output_key:
                self._set_data_in_store(output_key, output)
            if success:
                details = {"output_data_key": output_key} if output_key else {"file_path": task.get("file_path")}
                if isinstance(output, list):
                    details["records"] = len(output)
                log_audit_entry(self.audit_log, "SUCCESS", f"Task '{task_name}' completed successfully.",
                                task_type, details)
            else:
                log_audit_entry(self.audit_log, "ERROR", f"Task '{task_name}' failed.", task_type, task)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"An error occurred during task '{task_name}': {e}",
                            task_type, {"error": str(e), "task_details": task})
            logger.error(f"Error during task '{task_name}': {e}", exc_info=True)

    def _generate_audit_report(self, output_dir):
        ensure_directory_exists(output_dir)
        name = f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(output_dir, name)
        log_audit_entry(self.audit_log, "INFO", f"Audit report generated at {report_path}", "audit_report")
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.audit_log, f, indent=4, ensure_ascii=False)
            logger.info(f"Audit report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Failed to save audit report: {e}")
        return report_path

    def run(self):
        logger.info("Starting Data Agent run...")
        log_audit_entry(self.audit_log, "INFO", "Data Agent started.", "agent_run")
        for task in self.config.get("tasks", []):
            self._process_task(task)
        duration = (datetime.datetime.now() - self.start_time).total_seconds()
        log_audit_entry(self.audit_log, "INFO", f"Data Agent finished in {duration:.2f} seconds.",
                        "agent_run_summary")
        logger.info(f"Data Agent finished. Total time: {duration:.2f} seconds.")
        return self._generate_audit_report(os.path.join(self.base_dir, 'reports'))
```

## 8. `configs/data_pipeline_config.json`

```json
{
  "tasks": [
    {
      "name": "Load Sales Data CSV",
      "type": "load_csv",
      "file_path": "data/input_sales.csv",
      "output_data_key": "raw_sales_data"
    },
    {
      "name": "Aggregate Sales by Customer",
      "type": "transform_csv_aggregate",
      "input_data_key": "raw_sales_data",
      "output_data_key": "customer_sales_summary",
      "group_by_field": "Customer",
      "aggregate_field": "Amount",
      "aggregate_type": "sum"
    },
    {
      "name": "Save Aggregated Sales CSV",
      "type": "save_csv",
      "file_path": "data/processed_sales_by_customer.csv",
      "input_data_key": "customer_sales_summary",
      "fieldnames": ["Customer", "Total_Amount"]
    },
    {
      "name": "Convert Raw Sales to JSON",
      "type": "csv_to_json_conversion",
      "input_data_key": "raw_sales_data",
      "output_data_key": "raw_sales_json"
    },
    {
      "name": "Save Raw Sales JSON",
      "type": "save_json",
      "file_path": "data/sales_data.json",
      "input_data_key": "raw_sales_json",
      "indent": 4
    },
    {
      "name": "Load Inventory Data JSON",
      "type": "load_json",
      "file_path": "data/input_inventory.json",
      "output_data_key": "raw_inventory_data"
    },
    {
      "name": "Update Inventory Stock & Add Product",
      "type": "update_json_data",
      "input_data_key": "raw_inventory_data",
      "output_data_key": "updated_inventory_data",
      "updates": [
        {"path": "0.stock", "value": 75, "operation": "set"},
        {"path": "1.details.layout", "value": "UK ISO", "operation": "set"},
        {"path": "2.details.dpi", "value": 2000, "operation": "set"},
        {
          "path": "",
          "value": {
            "id": "PROD004",
            "name": "Smart Speaker",
            "category": "Audio",
            "stock": 40,
            "details": {
              "brand": "SoundGenius",
              "features": ["Voice Assistant", "Multi-room"]
            }
          },
          "operation": "add_to_list"
        },
        {"path": "PROD001.details.color", "value": "Space Grey", "operation": "set"}
      ]
    },
    {
      "name": "Query Specific Product Detail",
      "type": "query_json_data",
      "input_data_key": "updated_inventory_data",
      "output_data_key": "queried_product_brand",
      "path": "0.details.brand"
    },
    {
      "name": "Save Updated Inventory JSON",
      "type": "save_json",
      "file_path": "data/updated_inventory.json",
      "input_data_key": "updated_inventory_data",
      "indent": 2
    }
  ]
}
```

## 9. `data/input_sales.csv`

```csv
OrderID,Product,Amount,Price,Customer
101,Laptop,1200.50,1200.50,Alice
102,Mouse,25.00,25.00,Bob
103,Keyboard,75.25,75.25,Alice
104,Monitor,300.00,300.00,Charlie
105,Webcam,45.75,45.75,Bob
106,External HDD,90.00,90.00,David
107,Headphones,150.00,150.00,Alice
108,USB Hub,15.50,15.50,Eve
109,Gaming Mouse,60.00,60.00,Bob
110,SSD,200.00,200.00,Charlie
```

## 10. `data/input_inventory.json`

```json
[
  {
    "id": "PROD001",
    "name": "Laptop Pro",
    "category": "Electronics",
    "stock": 50,
    "details": {
      "brand": "TechCorp",
      "model": "XPS 15"
    }
  },
  {
    "id": "PROD002",
    "name": "Mechanical Keyboard",
    "category": "Peripherals",
    "stock": 120,
    "details": {
      "brand": "KeyMaster",
      "layout": "US ANSI"
    }
  },
  {
    "id": "PROD003",
    "name": "Ergonomic Mouse",
    "category": "Peripherals",
    "stock": 80,
    "details": {
      "brand": "ErgoGear",
      "dpi": 1600
    }
  }
]
```

## 11. `main.py`

```python
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
```

## 12. `.gitignore`

```text
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.ipynb_checkpoints/
.vscode/

# Environments
.env
.venv/
venv/
env/

# NOTE: output files in data/ and reports/ are intentionally committed for lab submission
```
