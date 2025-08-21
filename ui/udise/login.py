"""
Module: student_login

Description:
------------
This module automates the login process for the UDISE Student Module, including handling CAPTCHA validation,
credential verification, academic year selection, and dismissal of school information pop-ups. It is designed
to support robust UI automation with retry logic and logging for traceability.

Features:
---------
- Automated login with retry mechanism for invalid CAPTCHA or incorrect credentials.
- Check Main Page for status and 503 indicators
- Selection of academic year post-login.
- Graceful handling of UI interruptions such as school information dialogs.
- Logging of each step for debugging and audit purposes.

Dependencies:
-------------
- time: for introducing delays between UI actions.
- common.config.TIME_DELAY: configurable delay duration.
- common.logger.logger: logging utility for tracking actions.
- common.driver.driver: WebDriver instance for browser interaction.
- utils.utils.wait_and_click, wait_and_find_element: helper functions for UI interaction.
- ui.locators.udise.StudentImportLocator: locator definitions for UI elements.
- ui.udise.login: contains locator classes for academic year and school info elements.

Usage:
------
This module is intended to be used as part of a larger automation framework for UDISE.
It can be invoked to perform login operations and navigate through the initial setup steps
required to access student data.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-08-19

Version: 1.0.0
"""

import time

from common.driver import driver
from common.logger import logger
from ui.locators.udise import StudentLoginLocator
from utils.utils import wait_and_click, wait_and_find_element


class StudentLogin:
    """
    Handles login automation for the UDISE Student Module.

    This class provides methods to perform login operations with retry logic for invalid CAPTCHA
    or incorrect credentials, select the academic year post-login, and manage UI interruptions
    such as school information pop-ups.

    Methods:
    --------
    student_module_login(username, password, max_attempts=3):
        Attempts login with provided credentials, retrying on CAPTCHA or credential errors.

    select_academic_year():
        Selects the current academic year from the UI and closes any resulting pop-ups.

    close_school_info():
        Closes the school information dialog that may appear after academic year selection.

    invalid_captcha():
        Checks for CAPTCHA validation errors by inspecting UI messages.

    Notes:
    ------
    - Relies on utility functions like `wait_and_click` and `wait_and_find_element`.
    - Uses predefined locators such as `StudentLogin.USERNAME`, `StudentLogin.PASSWORD`, etc.
    - Includes logging for traceability and debugging.
    """

    def student_login(self, username, password, max_attempts=3):
        """
        Attempts to log in to the UDISE student module with retries for invalid CAPTCHA or incorrect credentials.

        Parameters:
            username (str): The username to authenticate with.
            password (str): The password associated with the username.
            max_attempts (int): Maximum number of login attempts before giving up.

        Raises:
            Exception: If login fails after max_attempts.
        """

        logger.info("Starting login to UDISE Student Module")
        locators = [
            (username, StudentLoginLocator.PASSWORD),
            (password, StudentLoginLocator.PASSWORD),
        ]

        for attempt in range(1, max_attempts + 1):
            logger.info(f"Login attempt {attempt}/{max_attempts}")
            # Fill credentials
            for value, locator in locators:
                elem = wait_and_find_element(locator)
                elem.clear()
                elem.send_keys(value)

            wait_and_click(StudentLoginLocator.CAPTCHA)

            logger.info("Waiting 15 seconds for manual CAPTCHA entry")
            time.sleep(15)

            wait_and_click(StudentLoginLocator.SUBMIT_BUTTON)
            logger.info("Clicked on the Submit button to initiate login")

            # Give UI a moment to render any error messages
            time.sleep(2)

            if self.invalid_captcha():
                logger.warning("Invalid CAPTCHA detected. Retrying login...")
                continue

            if self.incorrect_creds():
                logger.warning("Incorrect credentials detected. Retrying login...")
                continue

            # If no errors, assume login success
            logger.info("Login successful. Proceeding to academic year selection.")
            time.sleep(2)
            self.select_academic_year()
            return

        # If loop completes without successful login
        raise Exception(
            "Login failed after maximum attempts due to repeated CAPTCHA or credential errors."
        )

    def select_academic_year(self):
        """
        Selects the current academic year from the dropdown or list.

        This function locates and clicks on the academic year element using predefined
        locators. After selection, it closes any school information pop-up or modal
        that may appear as a result of the selection.

        Dependencies:
            - wait_and_click: Utility function to wait for and click UI elements.
            - AcademicChoiceLocators.ACADEMIC_YEAR: Locator for the academic year element.
            - close_school_info: Function to close school-related pop-ups.

        Returns:
            None
        """

        wait_and_click(StudentLoginLocator.ACADEMIC_YEAR)
        logger.info("Selected Current Academic Year")

        self.close_school_info()

    def close_school_info(self):
        """
        Closes the school information pop-up window if it appears.

        This function detects and dismisses the school information modal or overlay
        that may block further interaction with the page. It ensures smooth workflow
        by removing UI interruptions after academic year selection or login.

        Dependencies:
            - wait_and_click or equivalent method to interact with the close button.
            - Locator for the school info close button (e.g., SchoolInfoLocators.CLOSE_BUTTON).

        Returns:
            None

        Raises:
            Exception: If the pop-up cannot be closed due to missing elements or UI issues.
        """

        wait_and_click(StudentLoginLocator.SCHOOL_INFO)
        logger.info("Closed School Information dialog popup")
        time.sleep(1)

    def invalid_captcha(self):
        """
        Checks whether the CAPTCHA validation message indicates an invalid input.

        This function waits for the CAPTCHA message element to appear on the student login page,
        retrieves its inner HTML content, and returns True if the message contains the word "Invalid".

        Returns:
            bool: True if the CAPTCHA message contains "Invalid", False otherwise.
        """
        time.sleep(2)  # Give UI a moment to render error messages
        elements = driver.find_elements(*StudentLoginLocator.ERROR_ALERT)
        if elements:
            msg = elements[0].get_attribute("innerHTML")
            logger.info(f"CAPTCHA error message: {msg}")
            return "Invalid" in msg if msg else False
        return False

    def incorrect_creds(self):
        """
        Checks if the login failure was due to incorrect username or password.

        This function retrieves the inner HTML of the element associated with invalid login messages.
        It logs the message content and returns True if the message contains the keyword 'Incorrect',
        indicating a credential-related failure.

        Returns:
            bool: True if the message indicates incorrect credentials, False otherwise.
        """
        time.sleep(2)  # Give UI a moment to render error messages
        elements = driver.find_elements(*StudentLoginLocator.ERROR_ALERT)
        if elements:
            msg = elements[0].get_attribute("innerHTML")
            logger.info(f"Credential error message: {msg}")
            return "Incorrect" in msg if msg else False
        return False
