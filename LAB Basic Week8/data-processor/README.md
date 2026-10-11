# Lab Basic Week 8: Automating with CSV and JSON Data

A Python data processor that reads, transforms, filters and writes two structured plaintext
formats — **CSV** and **JSON** — using only Python's built-in `csv` and `json` modules.

## What the program does

**CSV workflow (sales data)**
1. Reads `data/input_sales.csv` with `csv.DictReader` (each row becomes a dictionary).
2. Converts `Amount` and `Price` from strings to `float`.
3. Calculates **total sales** and **average item price** across all orders.
4. Filters orders where `Amount >= 100`.
5. Writes the filtered rows plus a `SUMMARY` row to `data/output_filtered_sales.csv` with `csv.DictWriter`.

**JSON workflow (inventory data)**
1. Reads `data/input_inventory.json` with `json.load` (a list of nested product dictionaries).
2. Updates stock: `PROD001` → 60, `PROD003` → 75.
3. Adds a new product `PROD004` (Gaming Headset) with nested `details`.
4. Writes the result to `data/output_updated_inventory.json` with `json.dump(indent=2)`.

## Project structure

```
data-processor/
├── src/
│   ├── __init__.py          # Package marker
│   ├── csv_handler.py       # CSV read / write / process
│   ├── json_handler.py      # JSON read / write / update / add
│   └── utils.py             # Logging setup and directory helper
├── data/
│   ├── input_sales.csv                 # Sample input CSV
│   ├── input_inventory.json            # Sample input JSON
│   ├── output_filtered_sales.csv       # Generated output
│   └── output_updated_inventory.json   # Generated output
├── main.py                  # Runs both workflows
├── run_log.txt              # Console output from a sample run
├── .gitignore
└── README.md
```

## How to run

```bash
git clone https://github.com/YOUR_USERNAME/data-processor.git
cd data-processor

# optional: virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

python main.py
```

No `pip install` is needed — `csv`, `json`, `logging` and `os` are all built in.

## Results

`data/output_filtered_sales.csv`

| OrderID | Product    | Amount  | Price   | Customer |
|---------|------------|---------|---------|----------|
| 101     | Laptop     | 1200.50 | 1200.50 | Alice    |
| 104     | Monitor    | 300.00  | 300.00  | Charlie  |
| 107     | Headphones | 150.00  | 150.00  | Alice    |
| SUMMARY | Total/Avg  | 1902.00 | 237.75  | Count: 3 |

The SUMMARY row's total (1902.00) and average price (237.75) are computed over **all 8 orders**;
`Count: 3` is the number of orders that passed the `Amount >= 100` filter.

`data/output_updated_inventory.json` — stock levels after the run:

| ID      | Name                | Stock        |
|---------|---------------------|--------------|
| PROD001 | Laptop Pro          | 50 → **60**  |
| PROD002 | Mechanical Keyboard | 120          |
| PROD003 | Ergonomic Mouse     | 80 → **75**  |
| PROD004 | Gaming Headset      | **90 (new)** |

## Key concepts demonstrated

- **CSV reading/writing** with `DictReader` / `DictWriter`, including header handling and `QUOTE_MINIMAL` quoting.
- **Type conversion**: CSV values are always strings, so numbers are converted with `float()`.
- **Aggregation and filtering**: sum, average, and condition-based filtering.
- **JSON serialization/deserialization** with `json.load` / `json.dump`, pretty-printed with `indent`.
- **Nested data**: updating and adding entries inside a list of nested dictionaries.
- **Modular design**: CSV, JSON and utility logic live in separate modules.
- **Error handling**: missing files, invalid JSON, non-numeric values and missing keys are logged instead of crashing.

## Changes from the lab template

- Imports use `from utils import ...` (not `from .utils import ...`) because `main.py` adds `src/`
  to `sys.path`; the relative import in the template raises `ImportError`.
- Added `logger.propagate = False` so each log message prints once instead of twice.
- Header names are stripped of extra spaces and blank CSV lines are skipped.
- `add_product` refuses duplicate product IDs; `update_inventory` logs the old and new stock.
- Output files are committed as sample results (removed from `.gitignore`).

## Debugging notes

- **`FileNotFoundError` / "file not found"** — input files must be inside `data/`.
- **`KeyError`** — CSV header names must match `Amount`, `Price` exactly.
- **`json.JSONDecodeError`** — check for missing commas, unquoted keys or mismatched brackets; save as UTF-8.
- **`ValueError: could not convert string to float`** — remove symbols like `$` or `,` from numeric columns.
- **Strange characters** — read and write with `encoding='utf-8'`.
