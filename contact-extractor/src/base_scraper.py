from abc import ABC, abstractmethod
from typing import Set, Optional, Tuple
import logging
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.contact_page_keywords = [
            "contact",
            "about",
            "reach-us",
            "get-in-touch",
            "connect",
            "support",
            "kontakt",
            "contact-us",
        ]

    def _find_potential_contact_pages(self):
        """Find URLs that likely contain contact information."""
        potential_pages = []
        try:
            page_links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in page_links:
                try:
                    href = link.get_attribute("href")
                    link_text = link.text.lower()
                    if href and any(
                        keyword in href.lower() or keyword in link_text
                        for keyword in self.contact_page_keywords
                    ):
                        potential_pages.append(href)
                except Exception:
                    continue
            return potential_pages
        except Exception as e:
            logger.debug(f"Error finding contact pages: {str(e)}")
            return []

    def scrape_strategically(self, target_url: str) -> Tuple[Optional[str], str]:
        """Template method defining the scraping strategy."""
        logger.info(f"Checking main page: {target_url}")
        
        # Check main page first
        self.driver.get(target_url)
        main_page_results = self._collect_from_page()
        
        if main_page_results:
            best_result = self._process_results(main_page_results, target_url)
            if best_result:
                return best_result, target_url
                
        # Check contact pages if nothing found
        contact_links = self._find_potential_contact_pages()
        
        for link in contact_links:
            logger.info(f"Checking contact page: {link}")
            self.driver.get(link)
            contact_page_results = self._collect_from_page()
            
            if contact_page_results:
                best_result = self._process_results(contact_page_results, link)
                if best_result:
                    return best_result, link
                    
        return None, target_url
    
    @abstractmethod
    def _collect_from_page(self) -> Set[str]:
        """Collect all instances of the target data from current page."""
        pass
        
    @abstractmethod
    def _process_results(self, results: Set[str], source_url: str) -> Optional[str]:
        """Process and select the best result from candidates."""
        pass 