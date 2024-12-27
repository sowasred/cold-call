from utils import load_json, setup_logger
from scrapper import initialize_driver, scroll_to_load, extract_companies, fetch_company_details
import os

def main():
    print("Starting Homestar Scraper")
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    print("logs directory created")
    # Setup logger
    logger = setup_logger("logs/scraper.log")
    logger.info("Starting Homestar Scraper")
    print("logger setup")
    # Load configuration
    config = load_json("config/categories.json")
    print("config loaded")
    categories = config.get("result", {})
    print("categories loaded")
    print(categories)
    logger.info(f"Loaded {len(categories)} categories.")
    print("logger info")
    # Initialize WebDriver
    driver = initialize_driver()
    try:
        for category, subcategories in categories.items():
            logger.info(f"Processing category: {category}")
            print("processing category")
            print(subcategories)
            for subcategory_dict in subcategories:
                # Safer dictionary unpacking
                if not subcategory_dict or len(subcategory_dict) != 1:
                    logger.warning(f"Skipping invalid subcategory format: {subcategory_dict}")
                    continue
                
                name = next(iter(subcategory_dict.keys()))
                url = subcategory_dict[name]
                logger.info(f"Processing subcategory: {name} at {url}")
                
                driver.get(url)
                scroll_to_load(driver, name)
                companies = extract_companies(driver)
                print("companies extracted")
                print(companies)
                company_details = fetch_company_details(driver, companies)
                print("company details fetched")
                print(company_details)
    finally:
        driver.quit()
        logger.info("Scraper finished.")

if __name__ == "__main__":
    main()
