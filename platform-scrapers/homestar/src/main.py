from utils import load_json, setup_logger
from scraper import (
    initialize_driver,
    scroll_to_load,
    extract_companies,
    fetch_company_details,
)
import pandas as pd
import os
from datetime import datetime
import json
import sys


def format_company_data(companies, company_details):
    formatted_data = []
    # Convert company_details list to a dictionary with company names as keys
    company_details_dict = {company['name']: company for company in company_details}
    
    for company in companies:
        company_info = company_details_dict.get(company['name'], {})
        social_links = company_info.get('social_links', {})
        row = {
            'Company Name': company['name'],
            'Category': company.get('category', ''),
            'Subcategory': company.get('subcategory', ''),
            'Phone': company_info.get('phone_number', ''),
            'Email': company_info.get('email', ''),
            'Address': company_info.get('address', ''),
            'Website': company_info.get('website', ''),
            'Instagram': social_links.get('instagram', ''),
            'Facebook': social_links.get('facebook', ''),
            'Twitter': social_links.get('twitter', ''),
            'LinkedIn': social_links.get('linkedin', ''),
            'Rating': company_info.get('score', ''),
        }
        formatted_data.append(row)
    return formatted_data


def main():
    print("Starting Homestar Scraper")
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    print("logs directory created")
    # Setup logger
    logger = setup_logger("logs")
    logger.info("Starting Homestar Scraper")
    print("logger setup")
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config", "categories.json")
    # Add error handling
    try:
        config = load_json(config_path)
        print(f"Successfully loaded config from: {config_path}")
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    categories = config.get("result", {})
    print("categories loaded")
    print(categories)
    logger.info(f"Loaded {len(categories)} categories.")
    print("logger info")
    # Initialize WebDriver
    driver = initialize_driver()
    all_company_data = []
    try:
        for category, subcategories in categories.items():
            logger.info(f"Processing category: {category}")
            print("processing category")
            print(subcategories)
            for subcategory_dict in subcategories:
                # Safer dictionary unpacking
                if not subcategory_dict or len(subcategory_dict) != 1:
                    logger.warning(
                        f"Skipping invalid subcategory format: {subcategory_dict}"
                    )
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
                formatted_data = format_company_data(companies, company_details)
                for row in formatted_data:
                    row['Category'] = category
                    row['Subcategory'] = name
                all_company_data.extend(formatted_data)
            print("all company data")
            print(all_company_data)
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/homestar_data_{timestamp}.csv"
            df = pd.DataFrame(all_company_data)
            df.to_csv(output_file, index=False)
            logger.info(f"Data saved to {output_file}")
    finally:
        driver.quit()
        logger.info("Scraper finished.")


if __name__ == "__main__":
    main()
