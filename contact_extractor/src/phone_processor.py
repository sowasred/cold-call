import re
import logging
from typing import List, Optional, Set
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class PhoneProcessor:
    """Handles phone number validation, cleaning, and selection of the best matching phone number."""

    def __init__(self):
        # Basic pattern for international and local formats
        self.phone_pattern = re.compile(r'(?:\+?\d{1,4}[-.\s]?)?\(?\d{1,}\)?[-.\s]?\d{1,}[-.\s]?\d{1,}')
        
        # Common test/example phone numbers to avoid
        self.invalid_numbers = {
            "1234567890",
            "0000000000",
            "1111111111",
            "0123456789",
        }

    def clean_and_validate_phone(self, raw_phone: str) -> Optional[str]:
        """
        Clean and validate a single phone number.

        Args:
            raw_phone: The raw phone string to process

        Returns:
            Cleaned phone if valid, None otherwise
        """
        try:
            # Remove all non-numeric characters
            candidate = re.sub(r'[^\d]', '', raw_phone)
            
            logger.info(f"Cleaning phone: {candidate}")
            
            # If 11 digits and starts with 1, remove the 1
            if len(candidate) == 11 and candidate.startswith('1'):
                candidate = candidate[1:]
            
            # Basic validation
            if not self._is_valid_phone(candidate):
                return None
                
            return candidate

        except Exception as e:
            logger.debug(f"Error cleaning phone {raw_phone}: {str(e)}")
            return None

    def _is_valid_phone(self, phone: str) -> bool:
        """
        Validate phone number format specifically for Canadian numbers.
        """
        # Remove any non-digit characters
        digits_only = re.sub(r'[^\d]', '', phone)
        
        # Must be exactly 10 digits for Canadian numbers
        if len(digits_only) != 10:
            return False
            
        # Check against known invalid numbers
        if digits_only in self.invalid_numbers:
            return False
            
        return True

    def select_best_phone(self, phones: Set[str], page_url: str) -> Optional[str]:
        """
        For Canadian numbers, we can simply return the first valid number
        since they'll all be in the same format.
        """
        return next(iter(phones)) if phones else None

    def process_phones(self, raw_phones: List[str], page_url: str) -> Optional[str]:
        """
        Process a list of raw phone numbers and return the best matching one.

        Args:
            raw_phones: List of raw phone strings
            page_url: URL where phones were found

        Returns:
            str: Best matching phone or None if no valid phones found
        """
        # Clean and validate phones
        valid_phones = set()
        for raw_phone in raw_phones:
            logger.info(f"Processing phone: {raw_phone}")
            clean_phone = self.clean_and_validate_phone(raw_phone)
            if clean_phone:
                valid_phones.add(clean_phone)

        # Select and return the best phone
        return self.select_best_phone(valid_phones, page_url)