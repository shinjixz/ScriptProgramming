# web-scraping-intro/src/scraper.py
"""
Simple web scraper for the "Automate the Boring Stuff with Python" (2nd Edition) homepage.

Downloads the page with `requests`, parses it with `BeautifulSoup`,
and extracts the book title and the chapter titles (with their links).
"""
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Text patterns that identify table-of-contents entries on the homepage,
# e.g. "Introduction", "Chapter 1 – Python Basics", "Appendix A – Installing ..."
CHAPTER_PATTERN = re.compile(r"^(Introduction|Chapter\s+\d+|Appendix\s+[A-Z])\b")


class SimpleWebScraper:
    """A class to encapsulate basic web scraping functionality."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
    }

    def __init__(self, target_url, timeout=10):
        self.target_url = target_url
        self.timeout = timeout

    # ------------------------------------------------------------------ #
    # Step 1: Download
    # ------------------------------------------------------------------ #
    def _get_html_content(self):
        """Download the HTML content from the target URL. Returns None on error."""
        print(f"Downloading content from: {self.target_url}")
        try:
            response = requests.get(self.target_url, headers=self.HEADERS, timeout=self.timeout)
            response.raise_for_status()  # Raise HTTPError for 4xx / 5xx
            print(f"Successfully downloaded content. (Status code: {response.status_code})")
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e} - Status Code: {e.response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred - Could not connect to {self.target_url}")
        except requests.exceptions.Timeout:
            print("The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request error occurred: {e}")
        return None

    # ------------------------------------------------------------------ #
    # Step 2 + 3: Parse and extract
    # ------------------------------------------------------------------ #
    @staticmethod
    def _extract_book_title(soup):
        """
        Find the book title. Every find() result is checked for None before use.

        On this site the <h1> only says "2nd Edition", so the real book name
        comes from the page's <title> tag. If the <h1> holds the edition,
        it is added in brackets, e.g. "Automate the Boring Stuff with Python (2nd Edition)".
        """
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        h1 = soup.find("h1")
        h1_text = h1.get_text(strip=True) if h1 else ""

        if title:
            if h1_text and "edition" in h1_text.lower() and h1_text.lower() not in title.lower():
                return f"{title} ({h1_text})"
            return title
        if h1_text:
            return h1_text
        return "Book Title Not Found"

    def _extract_chapters(self, soup):
        """
        Find all table-of-contents links.

        Instead of relying on CSS classes (which can change), we look at every
        <a href="..."> tag and keep the ones whose text looks like a chapter title.
        """
        chapters = []
        seen = set()
        for link in soup.find_all("a", href=True):
            title = " ".join(link.get_text().split())  # normalise whitespace
            if not CHAPTER_PATTERN.match(title) or title in seen:
                continue
            seen.add(title)
            chapters.append({
                "title": title,
                "url": urljoin(self.target_url, link["href"]),  # relative -> absolute URL
            })
        return chapters

    def parse(self, html_content):
        """Parse an HTML string and return the scraped data as a dict."""
        soup = BeautifulSoup(html_content, "html.parser")
        return {
            "source_url": self.target_url,
            "book_title": self._extract_book_title(soup),
            "chapters": self._extract_chapters(soup),
        }

    def scrape_main_titles(self):
        """Download the page and extract the book title and chapter titles."""
        html_content = self._get_html_content()
        if not html_content:
            return None
        return self.parse(html_content)