# agentic-web-scraper/test_setup.py
"""Quick check that Python packages, the config and the browser driver all work."""
import os
import sys

print(f"Python {sys.version.split()[0]}")

try:
    import selenium
    import webdriver_manager  # noqa: F401
    print(f"[OK] selenium {selenium.__version__}, webdriver-manager installed")
except ImportError as e:
    print(f"[FAIL] {e}  ->  run: pip install -r requirements.txt")
    sys.exit(1)

from src.config_parser import ConfigParser
from src.driver_manager import DriverManager

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs", "example_site_config.json")
try:
    config = ConfigParser(config_path).load_config()
    print(f"[OK] config loaded: {config['start_url']}")
except Exception as e:
    print(f"[FAIL] config: {e}")
    sys.exit(1)

dm = DriverManager(headless=True)
driver = dm.get_driver()
if not driver:
    print("[FAIL] could not start Chrome")
    sys.exit(1)
try:
    driver.get(config["start_url"])
    print(f"[OK] browser opened page: {driver.title}")
finally:
    dm.quit_driver()

print("All checks passed. Now run: python main.py")
