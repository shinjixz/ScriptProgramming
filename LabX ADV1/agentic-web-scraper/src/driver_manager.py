# agentic-web-scraper/src/driver_manager.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverManager:
    """
    Manages the setup and teardown of Selenium WebDriver instances.
    Automates driver download if not present.
    """

    def __init__(self, browser_name='chrome', headless=True):
        self.browser_name = browser_name.lower()
        self.headless = headless
        self.driver = None

    def get_driver(self):
        """Initializes and returns a WebDriver instance."""
        if self.driver:
            return self.driver

        if self.browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--log-level=3')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            try:
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"webdriver-manager failed ({e}). Trying Selenium Manager...")
                try:
                    # Selenium 4.6+ can locate/download the driver by itself
                    self.driver = webdriver.Chrome(options=options)
                except Exception as e2:
                    print(f"Error setting up Chrome driver: {e2}")
                    print("Make sure Google Chrome is installed.")
                    return None

        elif self.browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument('--headless')
            try:
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                print(f"Error setting up Firefox driver: {e}")
                print("Make sure Mozilla Firefox is installed.")
                return None
        else:
            raise ValueError(f"Unsupported browser: {self.browser_name}. Choose 'chrome' or 'firefox'.")

        # Implicit wait: up to 10 seconds for elements to appear
        self.driver.implicitly_wait(10)
        return self.driver

    def quit_driver(self):
        """Quits the WebDriver instance if it's running."""
        if self.driver:
            self.driver.quit()
            self.driver = None
