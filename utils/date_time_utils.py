"""
time_utils.py

Utility functions for handling time and timestamp formatting within
the AutoEdu framework.

This module provides standardized methods for generating human-readable
timestamps, which are used across logging, reporting, and audit trail
components.
Designed to minimize external dependencies and avoid circular imports,
`time_utils` ensures consistent time formatting throughout the application.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-22
Last Modified: 2025-10-25

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


def convert_to_ddmmyyyy(date_input):
    """
    Converts a date string to DD/MM/YYYY format,
    intelligently detecting format.

    Args:
        date_input (str/ datetime.date): Input date.

    Returns:
        str: Date formatted as "DD/MM/YYYY".

    Raises:
        ValueError: If the date is invalid or unparseable.
    """
    try:
        # If already a date object, format directly
        if isinstance(date_input, date):
            return date_input.strftime("%d/%m/%Y")

        date_input = date_input.strip().lower()
        date_input = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_input)

        numeric_match = re.match(
            r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$", date_input)
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
        parsed_date = parser.parse(date_input, dayfirst=True)
        return parsed_date.strftime("%d/%m/%Y")

    except Exception as e:
        raise ValueError(f"Invalid date format: {date_input}") from e


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


def get_year_from_date(date_str):
    """
    Extracts the year from a date string in DD/MM/YYYY format.

    Args:
        date_str (str): Date string like '09/10/2025'

    Returns:
        str: Year part as string, e.g. '2025'
    """
    try:
        return date_str.strip().split("/")[-1].split()[0]
    except (AttributeError, IndexError):
        return None


def is_valid_admission_date(adm_date,
                            holiday_months=None,
                            date_format="%d/%m/%Y"):
    """
    Validates whether the given admission date falls within the
    academic window:
    - Between 01/04/YYYY and 30/08/YYYY
    - Where YYYY is:
        - current year if today is between April and December
        - current year - 1 if today is between January and March

    Args:
        adm_date (str or date): Admission date to validate
        holiday_months (list)[Optional]: List of Holiday Months
        date_format (str)[Optional]: Format of input string if adm_date is str

    Returns:
        bool: True if valid, False otherwise
    """
    # Check if admision date is None
    if not adm_date:
        return False

    # Convert string to date if needed
    if isinstance(adm_date, str):
        try:
            adm_date = convert_to_ddmmyyyy(adm_date)
            adm_date = datetime.strptime(adm_date, date_format).date()
        except ValueError:
            return False

    today = date.today()
    current_year = today.year if today.month >= 4 else today.year - 1

    start = date(current_year, 4, 1)
    end = date(current_year, 8, 30)

    # Reject if Holiday Month
    if holiday_months and adm_date.month in holiday_months:
        return False

    return start <= adm_date <= end


def generate_random_admission_date(holiday_months=None):
    """
    Generates a random admission date between April 1st and July 30th
    of the academic year, excluding any specified holiday month.

    Academic year logic:
    - If current month is April to December → use current year
    - If current month is January to March → use current year - 1

    Args:
        holiday_months (list)[Optional]: List of Holiday Months
    Returns:
        date: A randomly selected valid admission date in DD/MM/YYYY format.
    """
    # Default to empty list if no holiday months provided
    holiday_months = holiday_months or []

    today = date.today()

    # Determine academic year based on current month
    year = today.year if today.month >= 4 else today.year - 1

    # Define admission window: April 1st to July 30th
    start_date = date(year, 4, 1)
    end_date = date(year, 7, 30)

    # Generate all valid dates in range
    valid_dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
        if (start_date + timedelta(days=i)).month not in holiday_months
    ]

    # Fallback if no valid dates remain
    if not valid_dates:
        raise ValueError(
            "No valid admission dates available after excluding holiday month.")

        # Return a random valid date
    return convert_to_ddmmyyyy(random.choice(valid_dates))


def get_time_duration(start_time, end_time):
    """
    Calculates the duration between two datetime objects and returns it
    as a human-readable string in minutes and seconds.

    Parameters:
        start_time (datetime): The start timestamp.
        end_time (datetime): The end timestamp.

    Returns:
        str: Duration formatted as "X minutes Y seconds".
    """
    # Calculate the time difference
    duration = end_time - start_time

    # Convert total seconds to minutes and seconds
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    # Format the output string
    return f"{minutes} minutes {seconds} seconds"
