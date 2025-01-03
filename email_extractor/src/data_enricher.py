import pandas as pd
import logging
from pathlib import Path
from typing import Optional
from email_scraper import WebEmailScraper
from phone_scraper import WebPhoneScraper

logger = logging.getLogger(__name__)

class HomestarDataEnricher:
    """Enriches Homestar company data with email addresses."""
    
    def __init__(self, driver, input_csv_path: str):
        """
        Initialize the enricher with WebDriver and CSV path.
        
        Args:
            driver: Selenium WebDriver instance
            input_csv_path: Path to the Homestar CSV file
        """
        self.driver = driver
        self.email_scraper = WebEmailScraper(driver)
        self.phone_scraper = WebPhoneScraper(driver)
        self.df = pd.read_csv(input_csv_path)
        
    def process_companies(self):
        """Process all companies in the dataset."""
        # Process only companies with valid websites
        results = self.df.apply(
            lambda row: pd.Series(self._process_single_company(row))
            if pd.notna(row['Website']) else pd.Series({'Email': None, 'Phone': None}),
            axis=1
        )
        
        # Update the dataframe with results
        self.df['Email'] = results['Email']
        self.df['Phone'] = results['Phone']
    
    def _process_single_company(self, row: pd.Series) -> dict:
        """Process a single company and return its contact information."""
        website = row['Website']
        company_name = row['Company Name']
        
        try:
            # Extract email
            email, _ = self.email_scraper.scrape_strategically(website)
            
            # Extract phone
            phone, _ = self.phone_scraper.scrape_strategically(website)
                
            return {
                'Email': email,
                'Phone': phone
            }
            
        except Exception as e:
            logger.error(f"Error processing {company_name}: {str(e)}")
            return {
                'Email': None,
                'Phone': None
            }

    def save_results(self, output_path: Optional[str] = None) -> None:
        """
        Save the enriched data to a new CSV file.
        
        Args:
            output_path: Optional custom output path
        """
        if output_path is None:
            # Generate output path based on input file
            input_path = Path(self.input_csv_path)
            output_path = input_path.parent / f"{input_path.stem}_enriched{input_path.suffix}"
        
        self.df.to_csv(output_path, index=False)
        logger.info(f"Saved enriched data to {output_path}") 