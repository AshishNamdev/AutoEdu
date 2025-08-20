"""
Module: student_import_ui

This module provides UI automation functionality for interacting with the UDISE Student Import interface.
It includes logic to select specific import options such as Student Movement and Progression, and initiate
the student import process via predefined UI locators.

Dependencies:
- time: for introducing delays between UI actions
- common.config.TIME_DELAY: configurable delay duration
- common.logger.logger: logging utility for tracking actions
- utils.utils.wait_and_click: helper function to interact with UI elements
- ui.locators.udise.StudentImportLocator: locator definitions for UI elements

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-08-18

Version: 1.0.0
"""

import time

from common.config import TIME_DELAY
from common.logger import logger
from utils.utils import wait_and_click
from ui.locators.udise import StudentImportLocator


class StudentImportUI:
    """
    Handles UI interactions for the Student Import section of the UDISE module.

    Methods:
    --------
    select_import_options():
        Automates the selection of import-related options including Student Movement and Progression,
        followed by the Student Import module. Includes logging and configurable delays to ensure
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
            TimeoutException if any element is not clickable within the expected time.
        """

        locators = [
            (
                "Student Movement and Progression",
                StudentImportLocator.STUDENT_MOVEMENT_PROGRESSION,
            ),
            ("Import Module", StudentImportLocator.STUDENT_IMPORT_OPTION),
            ("Import Within State", StudentImportLocator.IN_STATE_IMPORT),
        ]

        # Select Student Movement and Progression option, Import Module from the list and Import Within State option
        for msg, locator in locators:
            wait_and_click(locator)
            logger.info(f"Selected {msg} option")
            logger.info("waiting for %s seconds", TIME_DELAY)
            time.sleep(TIME_DELAY)

    def import_student(self, student_pen, dob):

        # Click Import Go Button
        wait_and_click(StudentImportLocator.IMPORT_GO_BUTTON)
        logger.info("Selected Import Within State")
        logger.info("waiting for %s seconds", TIME_DELAY)
        time.sleep(TIME_DELAY)
