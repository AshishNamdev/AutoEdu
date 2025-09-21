"""
aadhaar_utils.py

Provides utilities for validating Aadhaar numbers using format checks and
the Verhoeff checksum algorithm. These functions ensure data integrity
before submission, transformation, or schema mapping in automation workflows.

Key Features:
- Format validation (12-digit numeric string)
- Verhoeff checksum verification (used by UIDAI)
- Designed for integration into onboarding, import, and validation pipelines

Usage Example:
    from common.aadhaar_utils import AadhaarValidator

    if AadhaarValidator.is_valid("123456789012"):
        # Proceed with import or mapping

References:
- UIDAI Aadhaar format: https://uidai.gov.in
- Verhoeff algorithm: https://en.wikipedia.org/wiki/Verhoeff_algorithm

Intended for use in AutoEdu and other scalable automation platforms.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-09-21
Last Modified: 2025-09-21

Version: 1.0.0
"""

import re


class AadhaarValidator:
    """Utility class for validating Aadhaar numbers."""

    _d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]

    _p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]

    _inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    @classmethod
    def is_valid(cls, aadhaar_number):
        """
        Validates an Aadhaar number using format and Verhoeff checksum.

        Args:
            aadhaar_number (str): The Aadhaar number to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not re.fullmatch(r"\d{12}", aadhaar_number):
            return False
        return cls._verhoeff_check(aadhaar_number)

    @classmethod
    def _verhoeff_check(cls, num: str) -> bool:
        """Returns True if the number passes Verhoeff checksum."""
        c = 0
        for i, item in enumerate(reversed(num)):
            c = cls._d[c][cls._p[i % 8][int(item)]]
        return c == 0
