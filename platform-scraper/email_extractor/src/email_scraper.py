from selenium.webdriver.common.by import By
import logging
import re
from email_processor import EmailProcessor

logger = logging.getLogger(__name__)


class WebEmailScraper:
    """A class to handle email extraction from web pages."""

    def __init__(self, driver):
        """Initialize the extractor with a webdriver instance."""
        self.driver = driver
        self.email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
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

    def find_potential_contact_pages(self):
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

    def scrape_emails_strategically(self, target_url):
        """
        Strategic email extraction with processing.

        Args:
            base_url: Target URL to scrape

        Returns:
            tuple: (best_email, source_url) where best_email might be None
        """
        logger.info(f"Checking main page: {target_url}")

        email_processor = EmailProcessor()

        # Check main page first
        self.driver.get(target_url)
        main_page_emails = self._collect_emails_from_page()

        if main_page_emails:
            best_email = email_processor.process_emails(main_page_emails, target_url)
            if best_email:
                logger.info(f"Found best email: {best_email} at {target_url}")
                return best_email, target_url

        # Check contact pages if no suitable email found
        contact_links = self.find_contact_links()

        for link in contact_links:
            logger.info(f"Checking contact page: {link}")
            self.driver.get(link)
            contact_page_emails = self._collect_emails_from_page()

            if contact_page_emails:
                best_email = email_processor.process_emails(contact_page_emails, link)
                if best_email:
                    return best_email, link

        return None, target_url

    def _collect_emails_from_page(self):
        """Aggregate emails found through all extraction methods."""
        emails = set()
        emails.update(self._extract_emails_from_text())
        emails.update(self._extract_emails_from_source())
        emails.update(self._extract_emails_from_elements())
        return list(emails)

    def _extract_emails_from_text(self):
        """Extract email addresses from visible page text."""
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            return set(self.email_regex.findall(body_text))
        except Exception as e:
            logger.debug(f"Error extracting emails from text: {str(e)}")
            return set()

    def _extract_emails_from_source(self):
        """Extract emails from page source."""
        try:
            page_source = self.driver.page_source
            return set(self.email_regex.findall(page_source))
        except Exception as e:
            logger.debug(f"Error extracting from page source: {str(e)}")
            return set()

    def _extract_emails_from_elements(self):
        """Extract emails from specific elements like contact forms or mailto links."""
        emails = set()
        try:
            # Check mailto links
            mailto_links = self.driver.find_elements(
                By.CSS_SELECTOR, "a[href^='mailto:']"
            )
            for link in mailto_links:
                href = link.get_attribute("href")
                if href:
                    email = href.replace("mailto:", "").split("?")[0]
                    if self.email_regex.match(email):
                        emails.add(email)

            # Check contact form fields
            email_inputs = self.driver.find_elements(
                By.CSS_SELECTOR,
                "input[type='email'], input[name*='email'], input[id*='email']",
            )
            for input_field in email_inputs:
                placeholder = input_field.get_attribute("placeholder")
                if placeholder and "@" in placeholder:
                    potential_emails = self.email_regex.findall(placeholder)
                    emails.update(potential_emails)

        except Exception as e:
            logger.debug(f"Error extracting from elements: {str(e)}")

        return emails
