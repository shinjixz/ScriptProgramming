# web-scraping-intro/main.py
"""Main entry point for the simple web scraping application."""
import os
import sys

# Add the 'src' directory to the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

from scraper import SimpleWebScraper  # noqa: E402
from data_processor import save_to_json  # noqa: E402

TARGET_URL = "https://automatetheboringstuff.com/2e/"
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "scraped_output.json")


def main():
    scraper = SimpleWebScraper(TARGET_URL)
    scraped_data = scraper.scrape_main_titles()

    if not scraped_data:
        print("Failed to scrape data.")
        return

    print("\n--- Scraped Data ---")
    print(f"Book Title: {scraped_data['book_title']}")
    print("\nChapter Titles:")
    if scraped_data["chapters"]:
        for i, chapter in enumerate(scraped_data["chapters"], start=1):
            print(f"{i:2}. {chapter['title']}")
    else:
        print("No chapter titles found.")
    print("--------------------")
    print(f"Total: {len(scraped_data['chapters'])} entries\n")

    save_to_json(scraped_data, OUTPUT_FILE)


if __name__ == "__main__":
    main()
