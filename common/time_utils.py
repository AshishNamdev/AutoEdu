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

Usage Example:
--------------
>>> from common.time_utils import get_timestamp
>>> print(get_timestamp())
'2025-08-22 01:41:00'

Notes:
------
- This module is intentionally decoupled from logging and config layers to prevent
  circular import issues.
- All time values are based on the system's local timezone unless explicitly handled.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-22
Last Modified: 2025-08-22

Version: 1.0.0
"""

from datetime import datetime


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
