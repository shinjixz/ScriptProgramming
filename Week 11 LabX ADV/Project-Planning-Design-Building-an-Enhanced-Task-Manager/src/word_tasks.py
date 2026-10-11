# agentic-document-automator/src/word_tasks.py
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from utils import setup_logging  # ✅ แก้จาก .utils เป็น utils

logger = setup_logging(__name__)

class WordTasks:
    """Handles advanced Word document operations for the Document Agent."""
    
    def __init__(self):
        logger.info("WordTasks initialized.")

    def _replace_placeholder_in_paragraph(self, paragraph, placeholder, value):
        """Replaces a single placeholder in a paragraph's runs."""
        if placeholder not in paragraph.text:
            return False  # Placeholder not found in this paragraph
        replaced = False
        for item in paragraph.runs:
            if placeholder in item.text:
                item.text = item.text.replace(placeholder, str(value))
                replaced = True
                logger.debug(f"Replaced '{placeholder}' with '{value}' in paragraph.")
        if not replaced and paragraph.runs:
            # Placeholder is split across several runs: merge text into the first run
            full_text = paragraph.text.replace(placeholder, str(value))
            paragraph.runs[0].text = full_text
            for item in paragraph.runs[1:]:
                item.text = ""
        return True

    @staticmethod
    def _normalize_placeholders(data_placeholders):
        """Ensures every key is wrapped as '{{KEY}}' so braces are replaced too."""
        normalized = {}
        for key, value in data_placeholders.items():
            key = str(key)
            if not (key.startswith("{{") and key.endswith("}}")):
                key = "{{" + key + "}}"
            normalized[key] = value
        return normalized

    @staticmethod
    def _fill_table(table, table_data):
        """Fills a python-docx table with rows; the first row is bold (header)."""
        for r_idx, row_data in enumerate(table_data):
            row = table.add_row()
            for c_idx, cell_data in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.text = str(cell_data)
                if r_idx == 0 and cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].bold = True

    @staticmethod
    def _new_table(document, cols):
        table = document.add_table(rows=0, cols=cols)
        try:
            table.style = 'Table Grid'
        except Exception:
            logger.warning("Style 'Table Grid' not available, using default table style.")
        return table

    def generate_report_from_template(self, template_path, output_path, data_placeholders, table_data=None):
        """
        Generates a Word document from a template, filling placeholders and optional table data.
        `data_placeholders` is a dictionary where keys are placeholders (e.g., '{{REPORT_TITLE}}') 
        and values are the replacement strings.
        `table_data` is a list of lists, where the first sub-list is the header row.
        """
        if not os.path.exists(template_path):
            logger.error(f"Word template not found: {template_path}")
            return False
        
        try:
            document = docx.Document(template_path)
            data_placeholders = self._normalize_placeholders(data_placeholders)
            
            # Replace placeholders in paragraphs
            for paragraph in document.paragraphs:
                for placeholder, value in data_placeholders.items():
                    self._replace_placeholder_in_paragraph(paragraph, placeholder, value)
            
            # Replace placeholders in table cells
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            for placeholder, value in data_placeholders.items():
                                self._replace_placeholder_in_paragraph(paragraph, placeholder, value)
            
            # Add dynamic table if provided
            if table_data:
                logger.info("Adding dynamic table to the document.")
                cols = len(table_data[0]) if table_data else 0
                table = self._new_table(document, cols)
                self._fill_table(table, table_data)

                anchor = None
                for paragraph in document.paragraphs:
                    if "{{TABLE_PLACEHOLDER}}" in paragraph.text:
                        anchor = paragraph
                        break

                if anchor is not None:
                    # Move the table to where the placeholder was, then drop the placeholder
                    anchor._element.addnext(table._tbl)
                    anchor._element.getparent().remove(anchor._element)
                else:
                    logger.warning("Table placeholder '{{TABLE_PLACEHOLDER}}' not found in template. Table appended to end.")

            # Save the new document
            document.save(output_path)
            logger.info(f"Report generated from template and saved to '{output_path}'.")
            return True
            
        except Exception as e:
            logger.error(f"Error generating report from template: {e}")
            return False

    def extract_text_from_word(self, docx_path):
        """Extracts all text from a Word document."""
        if not os.path.exists(docx_path):
            logger.error(f"Word document not found: {docx_path}")
            return None
        
        try:
            document = docx.Document(docx_path)
            full_text = []
            
            for para in document.paragraphs:
                full_text.append(para.text)
            
            # Also extract text from tables
            for table in document.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        row_text.append(cell.text)
                    full_text.append("\t".join(row_text))  # Tab-separated cell values
            
            logger.info(f"Text extracted from Word document: {docx_path}")
            return "\n".join(full_text)
            
        except Exception as e:
            logger.error(f"Error extracting text from Word document '{docx_path}': {e}")
            return None