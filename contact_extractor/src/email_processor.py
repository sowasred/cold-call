import re
import dns.resolver
from urllib.parse import urlparse
import logging
from typing import List, Optional, Set

logger = logging.getLogger(__name__)


class EmailProcessor:
    """Handles email validation, cleaning, and selection of the best matching email."""

    def __init__(self):
        self.email_pattern = re.compile(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )
        # Common disposable email domains to avoid
        self.disposable_domains = {
            "temp-mail.org",
            "tempmail.com",
            "example.com",
            "test.com",
        }

    def clean_and_validate_email(self, raw_email: str) -> Optional[str]:
        """
        Clean and validate a single email address.

        Args:
            raw_email: The raw email string to process

        Returns:
            Cleaned email if valid, None otherwise
        """
        try:
            # Convert to lowercase and trim whitespace
            candidate = raw_email.lower().strip()
            logger.info(f"Cleaning email: {candidate}")
            # Remove any surrounding punctuation or brackets
            candidate = re.sub(r'^[\[\(<{"\']|[\]\)>}"\']$', "", candidate)

            # Validate the cleaned email
            if self._is_valid_email(candidate):
                return candidate

        except Exception as e:
            logger.debug(f"Error cleaning email {raw_email}: {str(e)}")

        return None

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format and check for disposable domains.

        Args:
            email: Email address to validate

        Returns:
            bool: True if email is valid, False otherwise
        """
        logger.info(f"Validating email: {email}")
        if not self.email_pattern.match(email):
            return False

        domain = email.split("@")[1]
        if domain in self.disposable_domains:
            return False

        return True

    def _check_mx_record(self, domain: str) -> bool:
        """
        Check if domain has valid MX records.

        Args:
            domain: Domain to check

        Returns:
            bool: True if MX record exists, False otherwise
        """
        try:
            dns.resolver.resolve(domain, "MX")
            return True
        except Exception:
            return False

    def select_best_email(self, emails: Set[str], page_url: str) -> Optional[str]:
        """
        Select the best email from a set of candidates.

        Args:
            emails: Set of validated email addresses
            page_url: URL of the page where emails were found

        Returns:
            str: Best matching email or None if no suitable email found
        """
        if not emails:
            return None

        # Extract domain from page URL
        try:
            page_domain = urlparse(page_url).netloc.lower()
            if page_domain.startswith("www."):
                page_domain = page_domain[4:]
        except Exception:
            page_domain = ""

        # Priority scoring for emails
        scored_emails = []
        for email in emails:
            score = 0
            email_domain = email.split("@")[1]

            # Highest priority: matching domain
            if email_domain == page_domain:
                score += 100

            # Medium priority: has valid MX record
            if self._check_mx_record(email_domain):
                score += 50

            # Lower priority: common business email patterns
            if any(
                pattern in email.lower()
                for pattern in ["contact", "info", "hello", "support"]
            ):
                score += 25

            scored_emails.append((email, score))

        # Sort by score and return the highest scoring email
        if scored_emails:
            return sorted(scored_emails, key=lambda x: x[1], reverse=True)[0][0]

        # If no scoring criteria met, return the first email
        return list(emails)[0]

    def process_emails(self, raw_emails: List[str], page_url: str) -> Optional[str]:
        """
        Process a list of raw emails and return the best matching one.

        Args:
            raw_emails: List of raw email strings
            page_url: URL where emails were found

        Returns:
            str: Best matching email or None if no valid emails found
        """
        # Clean and validate emails
        valid_emails = set()
        for raw_email in raw_emails:
            logger.info(f"Processing email: {raw_email}")
            clean_email = self.clean_and_validate_email(raw_email)
            if clean_email:
                valid_emails.add(clean_email)

        # Select and return the best email
        return self.select_best_email(valid_emails, page_url)
