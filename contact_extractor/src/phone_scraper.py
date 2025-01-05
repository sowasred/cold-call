from typing import Optional, Set
from base_scraper import BaseScraper
from phone_processor import PhoneProcessor
import re
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class WebPhoneScraper(BaseScraper):
    def __init__(self, driver):
        super().__init__(driver)
        # Basic pattern - should be enhanced for your specific needs
        self.phone_regex = re.compile(r'\+?[\d\-\(\)\s]{10,}')
        self.phone_processor = PhoneProcessor()
        
    def _collect_from_page(self) -> Set[str]:
        """Collect phone numbers from the current page."""
        phones = set()
        try:
            # Extract from visible text
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            phones.update(self.phone_regex.findall(body_text))
            
            # Extract from tel: links
            tel_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href^='tel:']")
            for link in tel_links:
                href = link.get_attribute("href")
                if href:
                    phone = href.replace("tel:", "")
                    phones.add(phone)
                    
        except Exception as e:
            logger.debug(f"Error extracting phones: {str(e)}")
            
        return phones
        
    def _process_results(self, phones: Set[str], source_url: str) -> Optional[str]:
        """Process and select the best phone number."""
        return self.phone_processor.process_phones(list(phones), source_url) 