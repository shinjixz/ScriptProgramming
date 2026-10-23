# LabX BASIC: Automating Spreadsheets (Excel & Google Sheets)

This project demonstrates how to programmatically interact with Microsoft Excel `.xlsx` files using Python's `openpyxl` library. It reads sales data from an existing spreadsheet, calculates totals, and writes a formatted summary report to a new Excel file.

## Output Screenshot

![Output Sales Report](images/output_sales_report.png)

The generated `output_sales_report.xlsx` contains:

| Product Name | Quantity | Unit Price | Total Price |
| :----------- | -------: | ---------: | ----------: |
| Laptop       | 2        | 1200.50    | 2,401.00    |
| Mouse        | 5        | 25.00      | 125.00      |
| Keyboard     | 3        | 75.99      | 227.97      |
| Monitor      | 1        | 300.00     | 300.00      |
| Printer      | 1        | 150.00     | 150.00      |
| **Grand Total** |       |            | **3,203.97** |

## Key Concepts Demonstrated

* **`openpyxl` Library**: Core library for reading, writing, and modifying Excel `.xlsx` files.
* **Workbook & Worksheet Management**: Loading, creating, and saving workbooks; accessing and creating sheets.
* **Cell Manipulation**: Reading and writing cell values by coordinates or cell names.
* **Data Processing**: Iterating through rows and performing calculations (total per item, grand total).
* **Basic Formatting**: Fonts, fills, borders, alignment, and number formats.
* **Sheet Structure**: Merging cells and dynamically adjusting column widths.

## Project Structure

```
spreadsheet-automator/
├── src/
│   ├── __init__.py            # Python package marker
│   └── excel_processor.py     # Core logic for Excel reading/writing/processing
├── data/
│   ├── input_sales.xlsx       # Sample input Excel file
│   └── output_sales_report.xlsx  # Generated output Excel file
├── images/
│   └── output_sales_report.png   # Screenshot of the generated report
├── create_input.py            # Helper: generates the sample input file
├── main.py                    # Application entry point
├── .gitignore
└── README.md
```

## Setup & How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/shinjixz/spreadsheet-automator.git
   cd spreadsheet-automator
   ```

2. **Install dependencies** (a virtual environment is recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate

   pip install openpyxl
   ```

3. **Prepare input data**

   `data/input_sales.xlsx` must have the headers `Product Name`, `Quantity`, `Unit Price` in cells A1, B1, C1, with data starting from row 2.

   To generate the sample file automatically:
   ```bash
   python create_input.py
   ```

4. **Run the script**
   ```bash
   python main.py
   ```

   Expected terminal output:
   ```
   Starting sales data processing from 'data\input_sales.xlsx'...
   Workbook 'data\input_sales.xlsx' loaded successfully.
   New workbook 'new_workbook.xlsx' created.
   Workbook saved to 'data\output_sales_report.xlsx'.
   Sales report successfully generated and saved to 'data\output_sales_report.xlsx'.
   ```

## How It Works

1. Loads `data/input_sales.xlsx` and reads the active sheet.
2. Skips empty rows and rows with invalid numbers.
3. Calculates `Total Price = Quantity × Unit Price` for each row and accumulates the grand total.
4. Writes a new sheet named **Sales Report** with:
   * Green, bold, centered headers
   * Thin borders on all data cells
   * `#,##0.00` number format on totals
   * A merged, yellow-highlighted **Grand Total** row
   * Auto-adjusted column widths
5. Saves the result to `data/output_sales_report.xlsx`.

## Debugging Tips

* **`FileNotFoundError`**: Make sure `input_sales.xlsx` is in the `data` folder and the name matches exactly.
* **`InvalidFileException`**: The file may be corrupted or in the old `.xls` format, which `openpyxl` does not support. Save as `.xlsx`.
* **`TypeError` / `ValueError`**: Text found where a number was expected. The script skips such rows and prints a warning.
* **Data mismatches**: The script assumes the column order Product Name, Quantity, Unit Price.

## Google Sheets (Conceptual Overview)

Google Sheets can be automated through the Google Sheets API, typically with the `gspread` library. Unlike local `.xlsx` files, it requires OAuth 2.0 or a service account credential, and data is read and written over the network rather than from disk. Credential files must never be committed to Git.

## Extension Ideas

* Google Sheets integration with `gspread`
* Automated data validation
* Charts generated with `openpyxl.chart`
* Conditional formatting
* A simple GUI with `Tkinter`
* Exporting data to and from a database
