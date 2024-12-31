import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from email_extractor.src.email_scraper import WebEmailScraper
from email_extractor.src.email_processor import EmailProcessor

logger = logging.getLogger(__name__)

class HomestarEmailEnricher:
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
        self.df = pd.read_csv(input_csv_path)
        
    def process_companies(self) -> pd.DataFrame:
        """
        Process all companies in the CSV and find their emails.
        
        Returns:
            DataFrame with enriched email data
        """
        logger.info(f"Processing {len(self.df)} companies")
        
        # Process only companies with valid websites
        self.df['Email'] = self.df.apply(
            lambda row: self._process_single_company(row)
            if pd.notna(row['Website']) else None,
            axis=1
        )
        
        return self.df
    
    def _process_single_company(self, row: pd.Series) -> Optional[str]:
        """
        Process a single company and find its email.
        
        Args:
            row: DataFrame row containing company data
            
        Returns:
            str: Best matching email if found, None otherwise
        """
        company_name = row['Company Name']
        website = row['Website']
        
        logger.info(f"Processing {company_name} at {website}")
        
        try:
            email, source_url = self.email_scraper.scrape_emails_strategically(website)
            if email:
                logger.info(f"Found email {email} for {company_name}")
                return email
            else:
                logger.warning(f"No email found for {company_name}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing {company_name}: {str(e)}")
            return None
    
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