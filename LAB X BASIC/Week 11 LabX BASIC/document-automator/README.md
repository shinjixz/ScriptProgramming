# Week 11: Automating PDFs & Word Documents (LabX BASIC)

This project demonstrates how to automate common tasks involving PDF and Word documents
using Python. It leverages `PyPDF2` for PDF manipulation and `python-docx` for Word document
creation and modification.

## Screenshots (Results)

### `merged_output.pdf`
`dummy_doc1.pdf` + `dummy_doc2.pdf` merged into a single 2-page PDF.

![merged_output.pdf](screenshots/merged_output_pdf.png)

### `output_report.docx`
Text extracted from `input_article.pdf`, plus a heading, formatted text (bold / italic / centered) and a summary table.

![output_report.docx](screenshots/output_report_docx.png)

Console log from the run: [`screenshots/run_log.txt`](screenshots/run_log.txt)

## Key Concepts Demonstrated

* **PDF Text Extraction**: Reading text content from PDF files (`PdfReader`, `page.extract_text()`).
* **PDF Merging**: Combining multiple PDF files into a single document (`PdfWriter.add_page()`).
* **PDF Splitting**: `PDFProcessor.split_pdf()` splits a PDF into chunks of N pages.
* **Word Document Creation**: Programmatically generating new `.docx` files.
* **Adding Content to Word**: Inserting headings, paragraphs, formatted text (bold, italic, font size, alignment), and tables.
* **Modular Design**: PDF and Word logic are separated into `pdf_processor.py` and `word_processor.py`.
* **Robustness**: Error handling for file operations and library calls, with logging for workflow visibility.

## Setup & How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/document-automator.git
   cd document-automator
   ```

2. **Install dependencies** (virtual environment recommended):
   ```bash
   python -m venv .venv
   # Windows (PowerShell):  .venv\Scripts\Activate.ps1
   # macOS / Linux:         source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Input documents** (already included in `documents/`):
   * `input_article.pdf` – 2-page article whose text is extracted into the Word report.
   * `dummy_doc1.pdf`, `dummy_doc2.pdf` – one-line PDFs used for the merge example.

4. **Run the script:**
   ```bash
   python main.py
   ```
   The script will:
   * Extract text from `input_article.pdf`.
   * Create `documents/output_report.docx` containing the extracted text, a custom heading, and a summary table.
   * Merge `dummy_doc1.pdf` and `dummy_doc2.pdf` into `documents/merged_output.pdf`.

## Project Structure

```
document-automator/
├── src/
│   ├── __init__.py          # Python package marker
│   ├── pdf_processor.py     # PyPDF2 operations (extract, merge, split)
│   ├── word_processor.py    # python-docx operations (create, add content, format)
│   └── utils.py             # Utilities (logging, directory creation)
├── documents/
│   ├── input_article.pdf    # Sample PDF for text extraction
│   ├── dummy_doc1.pdf       # Sample PDF for merging
│   ├── dummy_doc2.pdf       # Sample PDF for merging
│   ├── output_report.docx   # Generated Word document
│   └── merged_output.pdf    # Generated merged PDF
├── screenshots/
│   ├── merged_output_pdf.png
│   ├── output_report_docx.png
│   └── run_log.txt
├── main.py                  # Entry point that orchestrates the tasks
├── requirements.txt
├── .gitignore
└── README.md
```

## Fixes Applied to the Lab's Starter Code

| Problem in starter code | Fix |
|---|---|
| `main.py` added `src/` to `sys.path` and imported `pdf_processor` directly, but the modules use relative imports (`from .utils import ...`) → `ImportError` | Import as a package: `from src.pdf_processor import PDFProcessor` |
| `range(0_int, ...)` in `split_pdf()` → `NameError` | `range(0, ...)` |
| `split_pdf()` called `ensure_directory_exists` without importing it | Added to the import |
| `datetime` imported only under `if __name__ == "__main__"` | Imported at top of `main.py` |
| `page.extract_text()` can return `None` on image-only pages → `TypeError` on `+` | `page.extract_text() or ""` |
| Column widths set only on columns are ignored by Word | Width is also set on each cell |
| `.gitignore` had comments on the same line as patterns (not valid in Git) | Comments moved to their own lines |

## Debugging Document Automation

* **`FileNotFoundError`**: Make sure the input PDFs are in `documents/` and the names match exactly.
* **`PyPDF2.errors.PdfReadError`**: The PDF may be corrupted, encrypted, or not a valid PDF.
* **Blank Word Document / Missing Content**: Image-based (scanned) PDFs have no selectable text, so extraction returns nothing.
* **Formatting Issues in Word**: Formatting is applied per *run*; font sizes use `Pt()`.
* **Logging Output**: Watch for `ERROR` and `WARNING` lines in the console.

## Extension Ideas (Future Work)

* Template-based document generation (replace `{{name}}`, `{{date}}` placeholders).
* Advanced PDF parsing with `pdfminer.six` or `PyMuPDF`.
* PDF ↔ image conversion, mail merge, document comparison, and search/indexing.
