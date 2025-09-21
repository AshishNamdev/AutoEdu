"""
time_utils.py

Utility functions for handling time and timestamp formatting within the AutoEdu framework.

This module provides standardized methods for generating human-readable timestamps,
which are used across logging, reporting, and audit trail components. Designed to
minimize external dependencies and avoid circular imports, `time_utils` ensures
consistent time formatting throughout the application.

Functions:
----------
- get_timestamp(): Returns the current timestamp in 'YYYY-MM-DD HH:MM:SS' format.

Notes:
------
- This module is intentionally decoupled from logging and config layers to prevent
    circular import issues.
- All time values are based on the system's local timezone unless explicitly handled.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-22
Last Modified: 2025-09-22

Version: 1.0.0
"""

import random
import re
from datetime import date, datetime, timedelta

from dateutil import parser


def get_timestamp(format=None):
    """
    Returns the current timestamp formatted for log entries.

    Format:
        DD-MM-YYYY - HH:MMAM/PM (e.g., "20-08-2025 - 03:45PM")

    Returns:
        str: A string representing the current date and time.
    """
    return (
        datetime.now().strftime(format)
        if format
        else datetime.now().strftime("%Y%m%d_%H%M%S")
    )


def convert_to_ddmmyyyy(date_str):
    """
    Converts a date string to DD/MM/YYYY format, intelligently detecting format.

    Args:
        date_str (str): Input date string.

    Returns:
        str: Date formatted as "DD/MM/YYYY".

    Raises:
        ValueError: If the date is invalid or unparseable.
    """
    try:
        date_str = date_str.strip().lower()
        date_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)

        numeric_match = re.match(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$", date_str)
        if numeric_match:
            first, second, year = map(int, numeric_match.groups())
            if first > 12:
                day, month = first, second
            elif second > 12:
                day, month = second, first
            else:
                day, month = first, second

            # Validate actual calendar date
            validated = date(year, month, day)
            return validated.strftime("%d/%m/%Y")

        # Fallback to parser
        parsed_date = parser.parse(date_str, dayfirst=True)
        return parsed_date.strftime("%d/%m/%Y")

    except Exception as e:
        raise ValueError(f"Invalid date format: {date_str}") from e


def random_date(start_date, end_date, date_format):
    """
    Generate a random date between start_date and end_date.

    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format (default).
        end_date (str): End date in 'YYYY-MM-DD' format (default).
        date_format (str): Format of input/output dates.

    Returns:
        str: Random date in the same format.
    """
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    delta = end - start
    random_days = random.randint(0, delta.days)
    result = start + timedelta(days=random_days)
    return result.strftime(date_format)
