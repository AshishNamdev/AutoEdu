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
Last Modified: 2026-01-13

Version: 1.0.0
"""

import time

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.support.ui import Select

from common.config import CLASS, PAGE_SIZE, SECTIONS, TIME_DELAY
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
        Selects Section Shift options in the UDISE Student Module UI.

        Steps:
            - Clicks on 'Class / Section Shift' option.
            - Logs the action.
            - Calls helper to select the section shift class.

        Raises:
            TimeoutException if any element is not clickable
                                    within the expected time.
        """
        try:
            UI.wait_and_click(
                StudentSectionShiftLocators.SECTION_SHIFT_OPTION)
            logger.info("Selected Class / Section Shift Option")
            self._select_section_shift_class()
        except Exception as e:
            logger.error("Error selecting Section Shift options: %s", str(e))
            raise

    def _select_section_shift_class(self):
        """
        Selects the specified class from the Class dropdown
        in the Section Shift UI.

        Raises:
            TimeoutException if the dropdown is not found
                                    within the expected time.
        """
        try:
            UI.wait_until_ready(
                StudentSectionShiftLocators.SELECT_CLASS_DROPDOWN)
            Select(
                UI.wait_and_find_element(
                    StudentSectionShiftLocators.SELECT_CLASS_DROPDOWN)
            ).select_by_value(CLASS)
            logger.info("Selected Class: %s", CLASS)

            UI.wait_and_click(StudentSectionShiftLocators.GO_BUTTON)
            logger.debug("Clicked on Go Button")
        except TimeoutException as e:
            logger.error("Error selecting Section Shift class: %s", str(e))
            raise

    def _get_total_students_count(self):
        """
        Retrieves the total number of students listed in the
        section shift data table.

        Returns:
            int: The total count of students in the table.

        Raises:
            ValueError: If the count cannot be converted to an integer.
        """
        logger.info("Retrieving total students count from UI...")
        logger.info("Waiting for %s seconds", TIME_DELAY)
        time.sleep(TIME_DELAY)

        count_text = UI.wait_and_find_element(
            StudentSectionShiftLocators.STUDENT_COUNT
        ).text.strip()
        try:
            student_count = int(count_text.split()[-1])
        except (ValueError, IndexError) as e:
            logger.error(
                "Failed to parse student count from text: %s", count_text)
            raise ValueError("Invalid student count format") from e

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
        if student_count == 0:
            logger.info("No students found, total pages = 0")
            return 0

        # Assuming PAGE_SIZE entries per page
        total_pages = (student_count + PAGE_SIZE - 1) // PAGE_SIZE
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
        try:
            table = UI.wait_and_find_element(
                StudentSectionShiftLocators.SECTION_SHIFT_TABLE)
            logger.debug("Section shift data table retrieved successfully.")
            return table
        except TimeoutException as e:
            logger.error("Failed to locate section shift data table: %s", e)
            raise

    def get_section_shift_table_rows(self, table):
        """
        Retrieve all row elements from the section shift data table.

        Args:
            table (WebElement): The table element containing student rows.

        Returns:
            List[WebElement]: A list of row elements in the table.
        """
        rows = UI.wait_and_find_elements(
            StudentSectionShiftLocators.TABLE_ROW, table)
        if not rows:
            logger.warning("No rows found in section shift data table.")
        else:
            logger.debug(
                "Retrieved %d rows from section shift data table.", len(rows))
        return rows

    def get_ui_student_pen_and_section(self, student_row):
        """
        Retrieves the Permanent Enrollment Number (PEN)
        and Section of a student from the given table row.

        Args:
            student_row (WebElement): The table row element for the student.
        Returns:
            tuple: A tuple containing the student's PEN and Section.
        """
        return (
            self._get_ui_student_pen(student_row),
            self._get_ui_student_section(student_row)
        )

    def _get_ui_student_pen(self, student_row):
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
        ).text.strip()

    def _get_ui_student_section(self, student_row):
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
        ).text.strip()

    def shift_section(self, student_pen, section, student_row):
        """
        Shift a student to a new section in the UDISE UI.

        Args:
            student_pen(str): The student's Permanent Enrollment Number.
            section (str): The section the student will be shifted into.
            student_row (WebElement): The table row element for the student.

        Side Effects:
            - Selects new section using Selenium.
            - Logs debug and info messages.
            - Updates section in the UI.
        """
        try:
            logger.info("Shifting Student PEN No: %s to Section: %s",
                        student_pen, section)
            self._select_new_section(section, student_row)

            logger.debug("Waiting for %s seconds", TIME_DELAY / 3)
            time.sleep(TIME_DELAY / 3)

            self._update_section(student_row)
        except ValueError as ve:
            logger.warning(
                "Validation error during student section shift: %s", ve)
        except (TimeoutException, NoSuchElementException) as se:
            logger.error(
                "UI error during section shift for PEN=%s: %s",
                student_pen, se)
        except Exception as e:
            logger.error(
                "Unexpected error during student section shift: %s", e)

    def _select_new_section(self, section, student_row):
        """
        Selects a new section for the given student row in the
        section shift UI.

        Args:
            section (str): The section key used to look up the
                corresponding value in SECTIONS.
            student_row (WebElement): The row element representing
                the student in the UI.
        Raises:
            KeyError: If the section key is not found in SECTIONS.
            TimeoutException: If the dropdown element is not found within
                                the wait period.

        Workflow:
            - Locates the "New Section" dropdown within the student row.
            - Selects the section using `select_by_value`.
            - Logs the selected section.

        Assumes:
            - `StudentSectionShiftLocators.NEW_SECTION` is defined.
            - `UI.wait_and_find_element()` is available to locate elements.
            - `SECTIONS` contains a mapping of section keys to dropdown values.
        """

        if section not in SECTIONS:
            raise KeyError(
                f"Section '{section}' not found in SECTIONS mapping.")
        try:
            Select(
                UI.wait_and_find_element(
                    StudentSectionShiftLocators.NEW_SECTION, student_row
                )).select_by_value(SECTIONS[section])
        except TimeoutException as e:
            logger.error(
                "Failed to locate New Section dropdown for section '%s': %s",
                section, e)
            raise

        logger.info("Selected New Section: %s", section)
        time.sleep(TIME_DELAY / 3)

    def _update_section(self, student_row):
        """
        Clicks the "Update" button for the given student row to
        apply a section change in the UI.

        Args:
            student_row (WebElement): The row element representing
                the student whose section is being updated.

        Raises:
            TimeoutException: If the Update button is not found within
                                the wait period.
            NoSuchElementException: If the Update button cannot be located.

        Workflow:
            - Locates the Update button within the provided student row.
            - Clicks the button to trigger the section update action.
            - Logs the action for debugging purposes.

        Assumes:
            - `StudentSectionShiftLocators.UPDATE_BUTTON` is defined.
            - `UI.wait_and_click()` is available to handle element
            presence and interaction.
        """
        try:
            UI.wait_and_click(
                StudentSectionShiftLocators.UPDATE_BUTTON,
                parent_element=student_row)
            logger.debug(
                "Clicked Update button for student row: %s", student_row)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(
                "Failed to click Update button for student row: %s", e)
            raise
        except Exception as e:
            logger.error(
                "Unexpected error while clicking Update button: %s", e)
            raise

    def get_section_shift_message(self):
        """
        Retrieves the inner HTML content of the student import success
        message element and clicks the OK button to close the dialog.

        Returns:
            str: The HTML string contained within the success message element.

        Raises:
            TimeoutException: If the success message element is not found
                                within the wait period.
            AttributeError: If the element does not support text extraction.
        """
        try:
            status_message = UI.wait_and_find_element(
                StudentSectionShiftLocators.STATUS_MESSAGE
            ).text.strip()

            logger.info("Section Shift Message: %s", status_message)

            self._confirm_section_shift()
            return status_message
        except TimeoutException as e:
            logger.error("Failed to locate section shift message: %s", e)
            raise
        except AttributeError as e:
            logger.error("Element does not support text extraction: %s", e)
            raise

    def _confirm_section_shift(self):
        """
        Confirm the section shift workflow by clicking the OK button
        in the success dialog.

        Raises:
            TimeoutException: If the OK button is not found within the wait period.
            ElementClickInterceptedException: If the OK button is obstructed or not clickable.

        Note:
            Ensure that the StudentSectionShiftLocators are correctly
            defined and visible before invoking this method.
        """
        try:
            UI.wait_and_click(StudentSectionShiftLocators.OK_BUTTON)
            logger.debug("Clicked OK button to confirm section shift.")
        except TimeoutException as e:
            logger.error(
                "Failed to locate OK button for section shift confirmation: %s", e)
            raise
        except ElementClickInterceptedException as e:
            logger.error(
                "OK button was not clickable due to obstruction: %s", e)
            raise

    def go_to_next_page(self):
        """
        Navigates to the next page in the section shift data table.

        Raises:
            TimeoutException: If the Next Page button is not found
                                within the wait period.
            ElementClickInterceptedException: If the button is
                                bstructed or not clickable.
        """
        try:
            logger.debug("Attempting to navigate to the next page...")
            UI.wait_and_click(StudentSectionShiftLocators.NEXT_PAGE_BUTTON)
            logger.info("Successfully navigated to the next page.")
        except TimeoutException as e:
            logger.error("Next Page button not found: %s", e)
            raise
        except ElementClickInterceptedException as e:
            logger.error("Next Page button not clickable: %s", e)
            raise
