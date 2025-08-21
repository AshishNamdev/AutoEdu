"""
Utility functions for Selenium-based browser automation.

This module provides helper functions to launch the browser, wait for elements,
and perform robust clicking actions with retry logic. It integrates with a shared
driver instance and configurable timeout settings.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-08-18

Version: 1.0.0

Functions:
    - launch_browser(url): Opens and maximizes the browser window.
    - login_user(): login user to the specified portal.
"""

import os
import shutil
from datetime import datetime

from common.driver import driver
from common.logger import logger


def launch_browser(url):
    """
    Launches the browser with the specified URL and maximizes the window.

    This function navigates the browser to the given URL using the global `driver` instance
    and maximizes the browser window to ensure full visibility of page elements.

    Parameters:
        url (str): The URL to open in the browser.

    Returns:
        None
    """
    logger.info("Opening Chrome Browser")

    driver.get(url)
    driver.maximize_window()


def get_timestamp(format="%d-%m-%Y - %I:%M:%S%p"):
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


def backup_file(src_path, backup_dir="backup"):
    """
    Creates a timestamped backup of the given file in the specified backup directory.

    Args:
        src_path (str): Path to the source file to back up.
        backup_dir (str): Directory where the backup will be stored. Defaults to 'backup'.

    Returns:
        str: Full path to the created backup file.

    Raises:
        IOError: If backup fails due to permission or disk issues.
    """
    if not os.path.isfile(src_path):
        logger.debug(f"Source file not found: {src_path}")
        return

    os.makedirs(backup_dir, exist_ok=True)

    base_name = os.path.basename(src_path)
    name, ext = os.path.splitext(base_name)
    timestamp = get_timestamp()  # Includes microseconds
    backup_name = f"{name}_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)

    logger.debug("%s --> %s", src_path, backup_path)
    shutil.copy2(src_path, backup_path)  # Preserves metadata
    return backup_path
