"""
A collection of utility functions for file handling, date formatting,
schema normalization, and test data generation. These helpers support
resilient automation workflows by standardizing inputs, preserving
data integrity, and simplifying schema transformations.

Included Functions:
- backup_file: Creates a timestamped backup of a file with metadata
                preservation.
- convert_to_ddmmyyyy: Converts various date formats to DD/MM/YYYY
                        using intelligent parsing.
- clean_column_labels: Normalizes or restores column labels for consistent
                        schema mapping.
- random_date: Generates a random date between two given dates in a specified
                        format.

Usage Scenarios:
- Preprocessing files before upload or transformation
- Standardizing date formats across UI, Excel, and JSON layers
- Mapping human-readable labels to internal schema keys
- Simulating realistic date ranges for test data

Dependencies:
- common.logger for structured logging
- common.time_utils.get_timestamp for timestamp generation
- Assumes `dateutil.parser` is available for natural language date parsing


Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-09-21

Version: 1.0.0
"""

import os
import random
import re
import shutil
from datetime import date, datetime, timedelta

from dateutil import parser

from common.logger import logger
from common.time_utils import get_timestamp


def backup_file(src_path, backup_dir="backup"):
    """
    Creates a timestamped backup of the given file in the specified
    backup directory.

    Args:
        src_path (str): Path to the source file to back up.
        backup_dir (str): Directory where the backup will be stored.
                            Defaults to 'backup'.

    Returns:
        str: Full path to the created backup file.

    Raises:
        IOError: If backup fails due to permission or disk issues.
    """
    if not os.path.isfile(src_path):
        logger.error("Source file not found: %s", src_path)
        return

    os.makedirs(backup_dir, exist_ok=True)

    base_name = os.path.basename(src_path)
    name, ext = os.path.splitext(base_name)
    timestamp = get_timestamp()  # Includes microseconds
    backup_name = f"{name}_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)

    logger.info("%s --> %s", src_path, backup_path)
    shutil.copy2(src_path, backup_path)  # Preserves metadata
    return backup_path


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


def clean_column_labels(column_name, restore=False):
    """
    Normalizes or restores column lables for consistent schema handling.

    This utility transforms column lables into a safe, JSON-compatible format
    by trimming whitespace, converting to lowercase, and replacing spaces with
    underscores.
    When `restore=True`, it restores the original display format
    by converting underscores to spaces and applying title casing.

    Args:
        column_name (str): The column name to be transformed.
        restore (bool, optional): If True, restores the transformation to
            produce a human-readable label. Defaults to False.

    Returns:
        str: A cleaned or restored column name,
            depending on the `restore` flag.

    Examples:
        clean_column_name("Student Name") → "student_name"
        clean_column_name("student_name", restore=True) → "Student Name"

    Notes:
        - Useful for mapping UI labels to internal keys and vice versa.
        - Ensures consistent naming across JSON, Excel, and UI layers.
    """
    return (
        column_name.strip().lower().replace(" ", "_")
        if not restore
        else column_name.strip().title().replace("_", " ")
    )


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
