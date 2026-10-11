# agentic-web-scraper/main.py
import os
import logging

from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent

# Show only warnings/errors so the terminal output stays clean
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
os.environ.setdefault("WDM_LOG", "0")  # silence webdriver-manager logs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    """Main entry point: load config, then run the scraping agent."""
    os.chdir(BASE_DIR)  # always save into this project's data/ folder
    config_file_path = os.path.join(BASE_DIR, 'configs', 'example_site_config.json')

    try:
        config = ConfigParser(config_file_path).load_config()

        # Set headless=False to watch the browser work (useful for debugging)
        agent = ScraperAgent(config, browser='chrome', headless=True)
        output_path = agent.run()

        if output_path:
            print(f"Successfully scraped {len(agent.scraped_products)} items "
                  f"and saved to {os.path.relpath(output_path)}")
        else:
            print("Scraping failed. See the messages above.")
    except FileNotFoundError as e:
        logging.error(f"Configuration file error: {e}")
    except ValueError as e:
        logging.error(f"Configuration validation error: {e}")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
