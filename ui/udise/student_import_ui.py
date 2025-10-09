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
- ui.locators.udise.StudentImportLocators: locator definitions for UI elements

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-09-22

Version: 1.0.0
"""

import time

from selenium.webdriver.support.ui import Select

from common.config import SECTIONS, TIME_DELAY
from common.logger import logger
from common.ui_handler import UIHandler as UI
from ui.locators.udise import StudentImportLocators


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
                StudentImportLocators.STUDENT_MOVEMENT_PROGRESSION,
            ),
            ("Import Module", StudentImportLocators.STUDENT_IMPORT_OPTION),
            ("Import Within State", StudentImportLocators.IN_STATE_IMPORT),
        ]

        for msg, locator in locators:
            UI.wait_and_click(locator)
            logger.info("Selected %s option", msg)
            # logger.debug("waiting for %s seconds", TIME_DELAY)
            # time.sleep(TIME_DELAY)

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
                (student_pen, StudentImportLocators.STUDENT_PEN),
                (dob, StudentImportLocators.DOB),
            ]
            UI.fill_fields(field_data)

            logger.info("Student PEN No: %s, DOB: %s", student_pen, dob)

            UI.wait_and_click(StudentImportLocators.IMPORT_GO_BUTTON)
            logger.debug("Clicked Import button")
            logger.debug("Waiting for %s seconds", TIME_DELAY)
            time.sleep(TIME_DELAY)
        except ValueError as ve:
            logger.warning("Validation error during student import: %s", ve)
        except Exception as e:
            logger.error("Unexpected error during student import: %s", e)

    def submit_import_data(self, student_class, section, doa):
        """
        Fills and submits the student import form with specified class,
        section, and date of admission.

        Parameters:
            student_class (str): The class value to select from the dropdown.
            section (str): The section value to select from the dropdown.
            doa (str): Date of admission in the expected input format
                        (e.g., 'DD/MM/YYYY').

        Workflow:
            - Selects the appropriate class and section from
                dropdowns using `select_by_value`.
            - Clears and inputs the date of admission into the
                corresponding field.
            - Clicks the import button to submit the form.
            - Clicks the Confirm button to import student.

        Assumes:
            - All locators are defined in `StudentImportLocators`.
            - `wait_and_find_element()` and `wait_and_click()` are
                utility functions that handle element presence and interaction.
        """
        for value, locator in [
            (student_class, StudentImportLocators.SELECT_CLASS),
            (SECTIONS[section], StudentImportLocators.SELECT_SECTION),
        ]:
            logger.debug("Selecting value %s for %s", value, locator)
            Select(UI.wait_and_find_element(locator)).select_by_value(value)

        UI.fill_fields([(doa, StudentImportLocators.DOA)])
        logger.debug("Entered Date of Admission: %s", doa)

        self.confirm_student_import()

    def confirm_student_import(self):
        """
        Automates the student import workflow by sequentially triggering
        the import, confirming the action, and acknowledging the success
        message.

        Steps:
            1. Clicks the 'Import' button to initiate the student data import.
            2. Clicks the confirmation button to proceed with the import.

        Raises:
            TimeoutException: If any of the expected elements are not found
                                within the wait period.
            ElementClickInterceptedException: If an element is obstructed
                                or not clickable.

        Note:
            Ensure that the StudentImportLocators selectors are correctly
            defined and visible before invoking this method.
        """
        for locator in [
            StudentImportLocators.IMPORT_BUTTON,
            StudentImportLocators.IMPORT_CONFIRM_BUTTON,
        ]:
            UI.wait_and_click(locator)
            logger.debug("Clicked element: %s", locator)

    def get_import_message(self):
        """
        Retrieves the inner HTML content of the student import success
        message element and clicks the OK button to close the dialog.

        Returns:
            str: The HTML string contained within the success message element.

        Raises:
            TimeoutException: If the success message element is not found
                                within the wait period.
            AttributeError: If the element does not support
                                'get_dom_attribute'.

        Note:
            This method assumes that the import flow has already been
            completed and the success message is visible in the DOM.
        """
        import_message = UI.wait_and_find_element(
            StudentImportLocators.IMPORT_SUCCES_MESSAGE
        ).get_attribute("innerHTML")
        logger.info("Import Success Message: %s", import_message)

        UI.wait_and_click(StudentImportLocators.IMPORT_OK_BUTTON)
        logger.debug("Clicked OK button on import success dialog")
        return import_message

    def get_pen_status(self):
        """
        Determines the outcome of the student import flow by waiting
        for either a DOB mismatch error or a successful status indicator.

        This method uses a shared timeout to monitor both possible UI outcomes:
        - If the DOB mismatch message appears, it returns 'dob_error'.
        - If the student status element appears, it returns 'success'.
        - If neither appears within the timeout, it returns 'none'.

        Returns:
            str: One of 'dob_error', 'success', or 'none'
                    based on which UI element appears first.
        """
        return UI.wait_for_first_match(
            locators={
                "dob_error": StudentImportLocators.DOB_MISMATCH_MESSAGE,
                "success": StudentImportLocators.STUDENT_STATUS,
            },
            timeout=12,
        )

    def get_ui_dob_status(self):
        """
        Retrieves the DOB mismatch status message from the UI.

        This method locates the DOM element associated with the DOB mismatch
        alert and extracts its inner HTML content.
        Used to verify whether the entered date of birth matches the
        expected value during student import validation.

        Returns:
            str: The inner HTML content of the DOB mismatch message element.

        Raises:
            NoSuchElementException: If the locator is not found on the page.
            WebDriverException: For general Selenium interaction failures.
        """
        dob_error_msg = UI.wait_and_find_element(
            StudentImportLocators.DOB_MISMATCH_MESSAGE
        ).get_attribute("innerHTML")
        logger.debug("DOB Mismatch Message: %s", dob_error_msg)

        UI.wait_and_click(StudentImportLocators.DOB_MISMATCH_OK_BUTTON)
        logger.debug("Clicked OK button on DOB mismatch dialog")
        time.sleep(2)

        return dob_error_msg

    def get_student_status(self):
        """
        Detects the student's import eligibility status based
        on UI color-coded indicators.

        Returns:
            str: One of the following status strings:
                - 'active_for_import' if greenBack container is found
                - 'active_elsewhere' if redBack container is found
                - 'unknown' if no status container is detected
        """
        status = {
            "greenBack": (
                "Dropbox-End Session (Due to Progression/TC- "
                "Active for Import / Status Not Known)"
            ),
            "redBack": "active",
        }

        try:
            status_element = UI.wait_and_find_element(
                StudentImportLocators.STUDENT_STATUS)
            class_name = status_element.get_attribute("class") or ""
            if "greenBack" in class_name:
                return status["greenBack"]
            elif "redBack" in class_name:
                return status["redBack"]
            else:
                return "unknown"
        except Exception as e:
            logger.error("%s", str(e))
            return "unknown"

    def get_student_current_school(self):
        """
        Retrieves the name of the curent school of the student from
        Current Schooling Details section.

        This function locates the UI element that displays the current
        school's name and returns its text content.

        Returns:
            str: The name of the currently selected school.
        """
        school_name = UI.wait_and_find_element(
            StudentImportLocators.CURRENT_SCHOOL
        ).get_attribute("innerHTML")
        logger.debug("Student's Current school : %s", school_name)
        return school_name

    def get_import_class(self):
        """
        Retrieves the class shown in the import dropdown.

        This function locates the UI element for class selection
        and returns its currently selected value.

        Returns:
            str: The value of the currently selected class.
        """
        class_value = Select(
            UI.wait_and_find_element(StudentImportLocators.SELECT_CLASS)
        ).first_selected_option.get_attribute("value")
        logger.debug("Currently selected import class : %s", class_value)
        return class_value
