# agentic-web-scraper/src/utils.py
import os
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)


def save_data_to_json(data, filename, directory='data'):
    """Saves a list of dictionaries to a JSON file. Returns the file path or None."""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return filepath
    except IOError as e:
        print(f"Error saving data to JSON file: {e}")
        return None


def wait_for_element(driver, by, value, timeout=10):
    """Waits for an element to be present and visible. Returns it or None."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        WebDriverWait(driver, timeout).until(EC.visibility_of(element))
        return element
    except (TimeoutException, NoSuchElementException):
        return None
    except WebDriverException:
        # e.g. an invalid selector for this locator type (CSS vs XPath)
        return None


def robust_click(driver, by, value, max_attempts=3, delay_between_attempts=2):
    """Attempts to click an element several times if it is not immediately clickable."""
    for attempt in range(max_attempts):
        try:
            element = wait_for_element(driver, by, value)
            if not element:
                return False
            element.click()
            return True
        except WebDriverException as e:
            print(f"Click attempt {attempt + 1} failed: {e.__class__.__name__}")
            if attempt < max_attempts - 1:
                time.sleep(delay_between_attempts)
    print(f"Failed to click element {value} after {max_attempts} attempts.")
    return False


def scroll_to_bottom(driver):
    """Scrolls to the bottom of the page (useful for lazy-loaded content)."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
