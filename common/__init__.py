"""
Utility functions for Selenium-based browser automation.

This module provides helper functions to launch the browser, wait for elements,
and perform robust clicking actions with retry logic. It integrates with a shared
driver instance and configurable timeout settings.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-18
Last Modified: 2025-08-18
Version: 1.0.0

Functions:
    - launch_browser(url): Opens and maximizes the browser window.
    - login_user(): login user to the specified portal.
"""

from common.config import MODULE, PASSWORD, PORTAL, URL, USERNAME
from common.driver import driver
from common.logger import logger

target = ""
if PORTAL == "udise":
    if MODULE == "student":
        target = "udise_student_module"
        from portals.udise.student_module import student_module_login
    if MODULE == "teacher":
        target = "udise_teacher_module"
        from portals.udise.teacher_module import teacher_module_login


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
    logger.info("opening Chrome browser")

    driver.get(url)
    driver.maximize_window()


def login_user():
    """
    Launches the browser and navigates to the login URL.

    This function initializes the browser session and opens the target URL
    defined in the configuration. It serves as the entry point for user login
    automation.

    Returns:
        None
    """
    launch_browser(URL)

    if target == "udise_student_module":
        student_module_login(USERNAME, PASSWORD)
    elif target == "udise_teacher_module":
        teacher_module_login(USERNAME, PASSWORD)
    elif target == "mpbse":
        pass
    elif tager == "edu3":
        pass
