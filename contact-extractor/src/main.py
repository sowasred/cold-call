import logging
import os
from datetime import datetime
import undetected_chromedriver as uc
from data_enricher import HomestarDataEnricher
import pandas as pd

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


def find_latest_csv(directory: str) -> str:
    """Find the most recent CSV file in the specified directory.
    
    Args:
        directory: Directory to search for CSV files
        
    Returns:
        Path to the most recent CSV file
        
    Raises:
        FileNotFoundError: If no CSV files exist in the directory
    """
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {directory}")
    
    return os.path.join(
        directory,
        max(csv_files, key=lambda x: os.path.getctime(os.path.join(directory, x)))
    )


def main():
    # Setup logging
    os.makedirs("logs", exist_ok=True)
    logger = setup_logger("logs")
    logger.info("Starting Homestar Email Enrichment")
    
    driver = None
    try:
        # Initialize driver
        driver = initialize_driver()
        
        # Find and validate input file
        input_dir = "input"
        os.makedirs(input_dir, exist_ok=True)
        
        try:
            input_path = find_latest_csv(input_dir)
            logger.info(f"Processing file: {input_path}")
        except FileNotFoundError as e:
            logger.error(f"Failed to find input CSV: {e}")
            return
        
        # Create enricher instance and process
        try:
            enricher = HomestarDataEnricher(driver, input_path)
            enricher.process_companies()
            
            # Save results back to the same file
            enricher.save_results(input_path)
            logger.info(f"Successfully updated {input_path} with email data")
            
        except pd.errors.EmptyDataError:
            logger.error("Input CSV file is empty")
        except Exception as e:
            logger.error(f"Error during enrichment process: {str(e)}")
            
    finally:
        if driver:
            driver.quit()
            logger.info("Driver closed")

if __name__ == "__main__":
    main()