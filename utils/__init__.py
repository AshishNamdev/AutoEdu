"""
A collection of utility functions for file handling and
schema normalization.
These helpers support resilient automation workflows by
standardizing inputs, preserving
data integrity, and simplifying schema transformations.

Included Functions:
- backup_file: Creates a timestamped backup of a file with metadata
                preservation.
- clean_column_labels: Normalizes or restores column labels for consistent
                schema mapping.

Usage Scenarios:
- Preprocessing files before upload or transformation
- Mapping human-readable labels to internal schema keys

Dependencies:
- common.logger for structured logging
- utils.date_time_utils.get_timestamp for timestamp generation
- Assumes `dateutil.parser` is available for natural language date parsing

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-09-22

Version: 1.0.0
"""

import os
import re
import shutil

from utils.date_time_utils import get_timestamp


def backup_file(src_path, logger, backup_dir="backup"):
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


def clean_na_keys(input_dict):
    """
    Cleans dictionary keys that match the 'NA_<number>' pattern by replacing them with 'NA'.
    All other keys are preserved as-is.

    Args:
        input_dict (dict): The original dictionary with keys potentially in 'NA_<number>' format.

    Returns:
        dict: A new dictionary with cleaned keys. Keys matching 'NA_<number>' are replaced with 'NA'.
              Other keys remain unchanged.

    Example:
        >>> clean_na_keys({'NA_12': 'x', 'EU_99': 'y', 'NA_abc': 'z'})
        {'NA': 'x', 'EU_99': 'y', 'NA_abc': 'z'}
    """
    return {
        re.sub(r"^NA_\d+$", "NA", key) if re.match(r"^NA_\d+$", key) else key: value
        for key, value in input_dict.items()
    }
