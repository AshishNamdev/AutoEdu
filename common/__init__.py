"""
Utility functions for Selenium-based browser automation.

This module provides helper functions to launch the browser, wait for elements,
and perform robust clicking actions with retry logic.
It integrates with a shared driver instance and configurable timeout settings.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-09-18

Version: 1.0.1

Functions:
    - launch_browser(url): Opens and maximizes the browser window.
    - login_user(): login user to the specified portal.
"""

from common.driver import WebDriverManager
from common.logger import logger


def launch_browser(url):
    """
    Launches the browser with the specified URL and maximizes the window.

    This function navigates the browser to the given URL using the global
    `driver` instance and maximizes the browser window to ensure full
    visibility of page elements.

    Parameters:
        url (str): The URL to open in the browser.

    Returns:
        None
    """
    logger.info("Opening Chrome Browser")
    driver = WebDriverManager.get_driver()
    driver.get(url)
    driver.maximize_window()
