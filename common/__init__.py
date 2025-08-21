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
