"""
Module: student_import_ui

This module provides UI automation functionality for interacting with
the UDISE Student Import interface. It includes logic to select specific
import options such as Student Movement and Progression, and initiate
the student import process via predefined UI locators.

Dependencies:
- time: for introducing delays between UI actions
- common.config.TIME_DELAY: configurable delay duration
- common.logger.logger: logging utility for tracking actions
- utils.utils.wait_and_click: helper function to interact with UI elements
- ui.locators.udise.StudentImportLocator: locator definitions for UI elements

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-08-22

Version: 1.0.0
"""

import time

from selenium.common.exceptions import TimeoutException

from common.config import TIME_DELAY
from common.logger import logger
from common.utils import wait_and_click, wait_and_find_element
from ui import fill_fields
from ui.locators.udise import StudentImportLocator


class StudentImportUI:
    """
    Handles UI interactions for the Student Import section of the UDISE module.

    Methods:
    --------
    select_import_options():
        Automates the selection of import-related options including
        Student Movement and Progression, followed by the
        Student Import module.
        Includes logging and configurable delays to ensure
        reliable execution.
    """

    def select_import_options(self):
        """
        Selects key import options in the UDISE Student Module UI.

        Steps:
        - Clicks on 'Student Movement and Progression'
        - Clicks on 'Import Module'
        - Clicks on 'Import Within State'

        Each step includes logging and a delay to ensure UI stability.

        Raises:
            TimeoutException if any element is not clickable
                                    within the expected time.
        """

        locators = [
            (
                "Student Movement and Progression",
                StudentImportLocator.STUDENT_MOVEMENT_PROGRESSION,
            ),
            ("Import Module", StudentImportLocator.STUDENT_IMPORT_OPTION),
            ("Import Within State", StudentImportLocator.IN_STATE_IMPORT),
        ]

        for msg, locator in locators:
            wait_and_click(locator)
            logger.info("Selected %s option", msg)
            logger.info("waiting for %s seconds", TIME_DELAY)
            time.sleep(TIME_DELAY)

    def import_student(self, student_pen, dob):
        """
        Automates the student import process by entering PEN and DOB,
        then triggering the import action.

        Args:
            student_pen (str): The student's Permanent Enrollment Number.
            dob (str): The student's date of birth in DD/MM/YYYY format.

        Side Effects:
            - Fills input fields using Selenium.
            - Logs debug and info messages.
            - Clicks the import button and waits for UI transition.
        """
        try:
            field_data = [
                (student_pen, StudentImportLocator.STUDENT_PEN),
                (dob, StudentImportLocator.DOB),
            ]
            fill_fields(field_data)

            logger.debug("Student PEN No: %s, DOB: %s", student_pen, dob)

            wait_and_click(StudentImportLocator.IMPORT_GO_BUTTON)
            logger.info("Selected Import Within State")
            logger.info("Waiting for %s seconds", TIME_DELAY)
            time.sleep(TIME_DELAY)

        except ValueError as ve:
            logger.warning("Validation error during student import: %s", ve)
        except Exception as e:
            logger.error("Unexpected error during student import: %s", e)

    def get_ui_dob_status(self):
        """
        Retrieves the DOB mismatch status message from the UI.

        This method locates the DOM element associated with the DOB mismatch
        alert and extracts its inner HTML content. Used to verify whether the entered
        date of birth matches the expected value during
        student import validation.

        Returns:
            str: The inner HTML content of the DOB mismatch message element.

        Raises:
            NoSuchElementException: If the locator is not found on the page.
            WebDriverException: For general Selenium interaction failures.
        """
        status = None
        try:
            status = wait_and_find_element(
                StudentImportLocator.DOB_MISMATCH_MESSAGE
            ).get_attribute("innerHTML")
        except TimeoutException as e:
            logger.error("Unexpected error during student import: %s", e)
        return status
