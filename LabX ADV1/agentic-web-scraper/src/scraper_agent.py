# agentic-web-scraper/src/scraper_agent.py
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)

from .driver_manager import DriverManager
from .data_models import Product
from .utils import wait_for_element, robust_click, save_data_to_json

logger = logging.getLogger(__name__)


class ScraperAgent:
    """
    An agentic web scraper that operates based on a provided configuration.
    Perceive (read the page) -> Act (extract, click next) -> Repeat until goal reached.
    """

    def __init__(self, config, browser='chrome', headless=True):
        self.config = config
        self.driver_manager = DriverManager(browser_name=browser, headless=headless)
        self.driver = None
        self.scraped_products = []
        self.max_pages = config.get("max_pages", 5)
        logger.info(f"Scraper Agent initialized for {config['start_url']}")

    # ---------- helpers ----------
    @staticmethod
    def _find_child(parent, selector):
        """Find a child element by CSS, falling back to XPath."""
        try:
            return parent.find_element(By.CSS_SELECTOR, selector)
        except (NoSuchElementException, WebDriverException):
            return parent.find_element(By.XPATH, selector)

    def _get_element_text(self, parent_element, selector):
        if not selector:  # null in config = field not on the page
            return None
        try:
            return self._find_child(parent_element, selector).text.strip() or None
        except (NoSuchElementException, StaleElementReferenceException, WebDriverException):
            return None

    def _get_element_attribute(self, parent_element, selector, attribute):
        if not selector:
            return None
        try:
            value = self._find_child(parent_element, selector).get_attribute(attribute)
            return value.strip() if value else None
        except (NoSuchElementException, StaleElementReferenceException, WebDriverException):
            return None

    def _parse_product_data(self, item_element):
        """Extracts product data from one item block using the config selectors."""
        s = self.config["item_data_selectors"]
        name = self._get_element_text(item_element, s.get("name"))
        price = self._get_element_text(item_element, s.get("price"))
        description = self._get_element_text(item_element, s.get("description"))
        url = self._get_element_attribute(item_element, s.get("url"), "href")
        image_url = self._get_element_attribute(item_element, s.get("image_url"), "src")

        if name and price:  # basic validation
            return Product(name=name, price=price, description=description,
                           url=url, image_url=image_url)
        return None

    # ---------- perceive + act ----------
    def scrape_page(self):
        """Scrapes all product items on the current page."""
        selector = self.config["item_container_selector"]
        item_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        if not item_elements:
            try:
                item_elements = self.driver.find_elements(By.XPATH, selector)
            except WebDriverException:
                item_elements = []

        logger.info(f"Found {len(item_elements)} items on {self.driver.current_url}")
        for item_element in item_elements:
            product = self._parse_product_data(item_element)
            if product:
                self.scraped_products.append(product.to_dict())
            else:
                logger.warning("Could not parse product data from an item element.")

    def _go_to_next_page(self):
        """Finds and clicks the 'next page' control. Returns True if it moved."""
        selector = self.config.get("pagination_selector")
        if not selector:
            return False

        by = By.CSS_SELECTOR
        button = wait_for_element(self.driver, by, selector, timeout=5)
        if not button:
            by = By.XPATH
            button = wait_for_element(self.driver, by, selector, timeout=5)
        if not (button and button.is_displayed() and button.is_enabled()):
            return False

        old_url = self.driver.current_url
        if not robust_click(self.driver, by, selector):
            return False
        # Wait until the page actually changed
        for _ in range(20):
            if self.driver.current_url != old_url:
                break
            time.sleep(0.25)
        return True

    def run(self):
        """Executes the scraping process. Returns the output file path or None."""
        self.driver = self.driver_manager.get_driver()
        if not self.driver:
            logger.error("Failed to get WebDriver. Exiting.")
            return None

        try:
            self.driver.get(self.config["start_url"])
            current_page = 1
            while current_page <= self.max_pages:
                print(f"Scraping page {current_page}...")
                self.scrape_page()

                if current_page == self.max_pages:
                    break  # goal reached
                time.sleep(self.config.get("delay_between_pages", 2))  # polite delay
                if not self._go_to_next_page():
                    logger.info("No next page found. Ending pagination.")
                    break
                current_page += 1
        except Exception as e:
            logger.critical(f"An unhandled error occurred during scraping: {e}")
        finally:
            self.driver_manager.quit_driver()

        return save_data_to_json(self.scraped_products, "scraped_products.json")
