"""
Automates the UDISE Student Import workflow using Selenium.

This module handles authentication and UI interactions required to initiate
and execute student data import tasks within the UDISE portal. It leverages
modular UI components and centralized configuration for secure credential
handling.

Features:
    - Logs into the UDISE portal using provided credentials.
    - Initializes the student import UI workflow.
    - Provides hooks for future expansion of import logic.

Usage:
    Instantiate `StudentImport` and call `init_student_import()`
    to begin the import process.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-12-11
Last Modified: 2026-01-09

Version: 1.0.0
"""

import time

from selenium.webdriver.support.ui import Select

from common.config import CLASS, SECTIONS, TIME_DELAY
from common.logger import logger
from ui.locators.udise import StudentSectionShiftLocators
from ui.ui_actions import UIActions as UI


class StudentSectionShiftUI:
    """
    Handles UI interactions for the Student Section Shift task
    of the UDISE student module.

    Methods:
    --------
    select_import_options():
        Automates the selection of import-related options including
        Student Movement and Progression, followed by the
        Student Import module.
        Includes logging and configurable delays to ensure
        reliable execution.
    """

    def select_section_shift_options(self):
        """
        Selects keSection Shift options in the UDISE Student Module UI.

        Steps:
        - Clicks on 'Class / Section Shift'


        includes logging and a delay to ensure UI stability.

        Raises:
            TimeoutException if any element is not clickable
                                    within the expected time.
        """
        UI.wait_and_click(
            StudentSectionShiftLocators.SECTION_SHIFT_OPTION)
        logger.info("Selected Class / Section Shift Option")
        self._select_section_shift_class()

    def _select_section_shift_class(self):
        """
        Selects the specified class from the Class dropdown
        in the Section Shift UI.

        Raises:
            TimeoutException if the dropdown is not found
                                    within the expected time.
        """
        Select(
            UI.wait_and_find_element(
                StudentSectionShiftLocators.SELECT_CLASS_DROPDOWN)
        ).select_by_value(CLASS)
        logger.info("Selected Class: %s", CLASS)
        UI.wait_and_click(StudentSectionShiftLocators.GO_BUTTON)
        logger.debug("Clicked on Go Button")

    def _get_total_students_count(self):
        """
        Retrieves the total number of students listed in the
        section shift data table.

        Returns:
            int: The total count of students in the table.

        Raises:
            ValueError: If the count cannot be converted to an integer.
        """
        count_text = str(UI.wait_and_find_element(
            StudentSectionShiftLocators.STUDENT_COUNT
        ).get_attribute("innerHTML"))
        student_count = int(count_text.split()[-1])
        logger.info("Total Students Count: %s", count_text)
        return student_count

    def get_total_pages(self):
        """
        Retrieves the total number of pages in the section shift data table.
        Returns:
            int: The total number of pages.
        Raises:
            ValueError: If the page count cannot be converted to an integer.
        """
        student_count = self._get_total_students_count()
        total_pages = (student_count + 9) // 10  # Assuming 10 entries per page
        logger.info("Total Pages Count: %s", total_pages)
        return total_pages

    def get_section_shift_data_table(self):
        """
        Retrieves the section shift data table element from the UI.

        Returns:
            WebElement: The section shift data table element.
        Raises:
            TimeoutException: If the table element is not found
                                within the wait period.
        """
        return UI.wait_and_find_element(
            StudentSectionShiftLocators.SECTION_SHIFT_TABLE
        )

    def get_section_shift_table_rows(self, table):
        """
        Retrieves the rows of the section shift data table.

        Returns:
            list: A list of WebElement objects representing the
                    rows in the table.
        """
        return UI.wait_and_find_elements(
            StudentSectionShiftLocators.TABLE_ROW, table
        )

    def get_ui_student_pen(self, student_row):
        """
        Retrieves the Permanent Enrollment Number (PEN)
        of a student from the given table row.

        Args:
            student_row (WebElement): The table row element for the student.
        Returns:
            str: The student's Permanent Enrollment Number (PEN).
        """
        return UI.wait_and_find_element(
            StudentSectionShiftLocators.STUDENT_PEN_UI_ROW, student_row
        ).get_attribute("innerHTML").strip()

    def get_ui_student_section(self, student_row):
        """
        Retrieves the Section of a student from the
        given table row.

        Args:
            student_row (WebElement): The table row element for the student.
        Returns:
            str: The student's Section.
        """
        return UI.wait_and_find_element(
            StudentSectionShiftLocators.STUDENT_SECTION_UI_ROW, student_row
        ).get_attribute("innerHTML").strip()

    def shift_section(self, student_pen, section, student_row):
        """
        Automates the student import process by entering PEN and DOB,
        then triggering the import action.

        Args:
            student_pen(str): The student's Permanent Enrollment Number.
            section (str): The section the student will be shifted into.

        Side Effects:
            - Fills input fields using Selenium.
            - Logs debug and info messages.
            - Clicks the import button and waits for UI transition.
        """
        try:
            logger.info("Student PEN No: %s, Section: %s",
                        student_pen, section)
            self._select_new_section(section, student_row)

            logger.debug("Waiting for %s seconds", TIME_DELAY)
            time.sleep(TIME_DELAY)

            self._update_section(student_row)
        except ValueError as ve:
            logger.warning("Validation error during student import: %s", ve)
        except Exception as e:
            logger.error("Unexpected error during student import: %s", e)

    def _select_new_section(self, section, student_row):
        """
        Selects a new section for the given student row in the
        section shift UI.

        Parameters:
            section (str): The section key used to look up the
                corresponding value in SECTIONS.
            student_row (WebElement): The row element representing
                the student in the UI.

        Workflow:
            - Locates the "New Section" dropdown within the student row.
            - Selects the section using `select_by_value`.
            - Logs the selected section.

        Assumes:
            - `StudentSectionShiftLocators.NEW_SECTION` is defined.
            - `UI.wait_and_find_element()` is available to locate elements.
            - `SECTIONS` contains a mapping of section keys to dropdown values.
        """

        Select(
            UI.wait_and_find_element(
                StudentSectionShiftLocators.NEW_SECTION, student_row
            )).select_by_value(SECTIONS[section])
        logger.info("Selected New Section: %s", section)
        time.sleep(TIME_DELAY)
        self._update_section(student_row)

    def _update_section(self, student_row):
        """
        Clicks the "Update" button for the given student row to
        apply a section change in the UI.

        Parameters:
            student_row (WebElement): The row element representing
                the student whose section is being updated.

        Workflow:
            - Locates the Update button within the provided student row.
            - Clicks the button to trigger the section update action.
            - Logs the action for debugging purposes.

        Assumes:
            - `StudentSectionShiftLocators.UPDATE_BUTTON` is defined.
            - `UI.wait_and_click()` is available to handle element
            presence and interaction.
        """

        UI.wait_and_click(
            StudentSectionShiftLocators.UPDATE_BUTTON, student_row)
        logger.debug("Clicked Update Button")

    def get_section_shift_message(self):
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
        status_message = UI.wait_and_find_element(
            StudentSectionShiftLocators.STATUS_MESSAGE
        ).get_attribute("innerHTML")
        logger.info("Section Shift Message: %s", status_message)

        self._confirm_section_shift()
        return status_message

    def _confirm_section_shift(self):
        """
        Automates the student section shift workflow by
        confirming the action, and acknowledging the success
        message.

        Clicks the confirmation button to proceed with the import.

        Raises:
            TimeoutException: If any of the expected elements are not found
                                within the wait period.
            ElementClickInterceptedException: If an element is obstructed
                                or not clickable.

        Note:
            Ensure that the StudentSectionShiftLocators are correctly
            defined and visible before invoking this method.
        """
        UI.wait_and_click(StudentSectionShiftLocators.OK_BUTTON)
        logger.debug("Clicked Okay Button")

    def go_to_next_page(self):
        """
        Navigates to the next page in the section shift data table.

        Raises:
            TimeoutException: If the Next Page button is not found
                                within the wait period.
            ElementClickInterceptedException: If the button is obstructed
                                or not clickable.
        """
        UI.wait_and_click(StudentSectionShiftLocators.NEXT_PAGE_BUTTON)
        logger.debug("Navigated to the next page")
