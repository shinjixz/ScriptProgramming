# data-processor/main.py
import os
import sys

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from csv_handler import CSVHandler
from json_handler import JSONHandler
from utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)

DEFAULT_CSV_FIELDNAMES = ['OrderID', 'Product', 'Amount', 'Price', 'Customer']


def run_csv_workflow(csv_proc, input_path, output_path, min_amount=100.0):
    logger.info("--- Starting CSV Data Processing Workflow ---")

    # 1. Read CSV data
    sales_data = csv_proc.read_csv_as_dicts(input_path)
    if not sales_data:
        logger.error("No sales data to process from CSV.")
        return

    # 2. Process sales data (filter Amount >= min_amount and get summary)
    results = csv_proc.process_sales_data(sales_data, min_sale_amount=min_amount)
    filtered_sales = results["filtered_sales"]
    sales_summary = results["summary"]
    logger.info(f"Summary of all sales: {sales_summary}")

    # 3. Prepare data for writing, including a summary row
    csv_fieldnames = list(sales_data[0].keys()) or DEFAULT_CSV_FIELDNAMES
    summary_row = {
        'OrderID': 'SUMMARY',
        'Product': 'Total/Avg',
        'Amount': sales_summary['Total Sales'],
        'Price': sales_summary['Average Item Price'],
        'Customer': f"Count: {sales_summary['Filtered Sales Count']}",
    }

    # 4. Write filtered sales data to a new CSV
    csv_proc.write_dicts_to_csv(filtered_sales + [summary_row], output_path, csv_fieldnames)


def run_json_workflow(json_proc, input_path, output_path):
    logger.info("--- Starting JSON Data Processing Workflow ---")

    # 1. Read JSON inventory data
    inventory_data = json_proc.read_json(input_path)
    if not inventory_data:
        logger.error("No inventory data to process from JSON.")
        return

    # 2. Update existing product stock
    json_proc.update_inventory(inventory_data, "PROD001", 60)  # Laptop Pro
    json_proc.update_inventory(inventory_data, "PROD003", 75)  # Ergonomic Mouse

    # 3. Add a new product (nested structure)
    new_product_entry = {
        "id": "PROD004",
        "name": "Gaming Headset",
        "category": "Audio",
        "stock": 90,
        "details": {
            "brand": "SoundBlaster",
            "features": ["Noise Cancelling", "RGB"],
        },
    }
    json_proc.add_product(inventory_data, new_product_entry)

    # 4. Write updated JSON data to a new file (pretty-printed)
    json_proc.write_json(inventory_data, output_path, indent=2)


def main():
    """Main entry point for the CSV and JSON data processor."""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    ensure_directory_exists(data_dir)

    run_csv_workflow(
        CSVHandler(),
        os.path.join(data_dir, 'input_sales.csv'),
        os.path.join(data_dir, 'output_filtered_sales.csv'),
        min_amount=100.0,
    )
    run_json_workflow(
        JSONHandler(),
        os.path.join(data_dir, 'input_inventory.json'),
        os.path.join(data_dir, 'output_updated_inventory.json'),
    )

    logger.info("--- Data Processing Workflows Completed ---")


if __name__ == "__main__":
    main()
