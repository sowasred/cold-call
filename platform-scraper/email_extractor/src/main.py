import json
import os
import logging
from datetime import datetime
import undetected_chromedriver as uc
from email_scraper import WebEmailScraper


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)


def setup_logger(log_dir):
    """Setup logger with both latest and timestamped log files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    latest_log = f"{log_dir}/latest.log"
    timestamped_log = f"{log_dir}/scraper_{timestamp}.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    timestamp_handler = logging.FileHandler(timestamped_log)
    timestamp_handler.setFormatter(formatter)
    logger.addHandler(timestamp_handler)

    latest_handler = logging.FileHandler(latest_log, mode="w")
    latest_handler.setFormatter(formatter)
    logger.addHandler(latest_handler)

    return logger


def initialize_driver():
    """Initialize and return the Selenium WebDriver."""
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    )
    options.add_argument("--window-size=1440,900")

    return uc.Chrome(options=options)


def main():
    # Setup logging
    os.makedirs("logs", exist_ok=True)
    logger = setup_logger("logs")
    logger.info("Starting Email Scraper")

    # Initialize driver
    driver = initialize_driver()

    try:
        extractor = WebEmailScraper(driver)

        # Now we only need the base URLs
        urls = load_json("config/websites.json")

        results = {}
        for url in urls:
            logger.info(f"Processing base URL: {url}")
            emails, source_url = extractor.scrape_emails_strategically(url)

            if emails:
                logger.info(f"Found {len(emails)} emails at {source_url}: {emails}")
                results[url] = {"emails": emails, "found_at": source_url}
            else:
                logger.info(f"No emails found for {url}")
                results[url] = {"emails": [], "found_at": None}

    finally:
        driver.quit()
        logger.info("Email scraper finished")


if __name__ == "__main__":
    main()
