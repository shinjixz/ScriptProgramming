# web-scraping-intro/src/data_processor.py
"""Helpers for saving scraped data to disk."""
import json
import os


def save_to_json(data, output_path):
    """Save scraped data to a JSON file (creates the folder if needed)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved scraped data to: {output_path}")
