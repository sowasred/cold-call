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
            # Remove all non-numeric characters except + for international prefix
            candidate = re.sub(r'[^\d+]', '', raw_phone)
            
            logger.info(f"Cleaning phone: {candidate}")
            
            # Basic validation
            if not self._is_valid_phone(candidate):
                return None
                
            # Format number consistently
            # Keep + prefix if exists, otherwise assume local number
            if candidate.startswith('+'):
                formatted = candidate
            else:
                # You might want to add default country code here
                formatted = candidate
                
            return formatted

        except Exception as e:
            logger.debug(f"Error cleaning phone {raw_phone}: {str(e)}")
            return None

    def _is_valid_phone(self, phone: str) -> bool:
        """
        Validate phone number format and check against known invalid numbers.

        Args:
            phone: Phone number to validate

        Returns:
            bool: True if phone is valid, False otherwise
        """
        # Remove any non-digit characters except + for checking length
        digits_only = re.sub(r'[^\d+]', '', phone)
        
        # Basic validation rules
        if not digits_only:
            return False
            
        # Check minimum/maximum length (adjust these values based on your needs)
        if len(digits_only) < 10 or len(digits_only) > 15:
            return False
            
        # Check against known invalid numbers
        if digits_only in self.invalid_numbers:
            return False
            
        return True

    def select_best_phone(self, phones: Set[str], page_url: str) -> Optional[str]:
        """
        Select the best phone number from a set of candidates.

        Args:
            phones: Set of validated phone numbers
            page_url: URL of the page where phones were found

        Returns:
            str: Best matching phone or None if no suitable phone found
        """
        if not phones:
            return None

        # Priority scoring for phone numbers
        scored_phones = []
        for phone in phones:
            score = 0
            
            # Prefer international format
            if phone.startswith('+'):
                score += 50
                
            # Prefer longer numbers (more likely to be complete)
            digits = len(re.sub(r'[^\d]', '', phone))
            if digits >= 11:  # International format with country code
                score += 30
            elif digits == 10:  # Local format
                score += 20
                
            # Avoid obviously fake numbers
            if any(phone.endswith(str(i * 4)) for i in range(10)):
                score -= 50
                
            scored_phones.append((phone, score))

        # Sort by score and return the highest scoring phone
        if scored_phones:
            return sorted(scored_phones, key=lambda x: x[1], reverse=True)[0][0]

        # If no scoring criteria met, return the first phone
        return list(phones)[0]

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