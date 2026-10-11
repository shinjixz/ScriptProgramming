# spreadsheet-automator/create_input.py
# Helper script: creates data/input_sales.xlsx with sample sales data.
import os
import openpyxl


def create_input_file(path=os.path.join('data', 'input_sales.xlsx')):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    rows = [
        ("Product Name", "Quantity", "Unit Price"),
        ("Laptop", 2, 1200.50),
        ("Mouse", 5, 25.00),
        ("Keyboard", 3, 75.99),
        (None, None, None),  # Empty row to show the script skips it
        ("Monitor", 1, 300.00),
        ("Printer", 1, 150.00),
    ]
    for r in rows:
        ws.append(r)
    wb.save(path)
    print(f"Sample input file created at '{path}'.")


if __name__ == "__main__":
    create_input_file()
