"""
Automates the UDISE Student Section Shift workflow using Selenium.

This module handles UI interactions required to initiate
Student Section Shift task and execute section shifting task within the
UDISE portal Student Module. It leverages modular UI components and centralized
configuration.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-12-09
Last Modified: 2026-01-19

Version: 1.0.0
"""

import os
import time

from common.config import CLASSES, TIME_DELAY
from common.logger import logger
from common.student_data import StudentData
from portals.udise import Student
from ui.udise.section_shift_ui import StudentSectionShiftUI
from utils.parser import StudentDataParser
from utils.report import ReportExporter


class StudentSectionShift:
    """
    Handles the Student Section Shift task within the UDISE portal.

    This class encapsulates the logic required to perform section shifting
    for students by interacting with the UDISE portal's UI components.

    Attributes:
        None
    """

    def __init__(self):
        self.section_shift_ui = StudentSectionShiftUI()
        self.student_data = None
        self.shifted_students = []

    def _prepare_section_shift_data(self):
        """
        Prepares and retrieves student section shift data.

        This method initializes a StudentDataParser instance,
        parses the input data, and returns the structured student data
        ready for further processing or storage.

        Returns:
            None
        """
        section_shift_data_file = os.path.join(
            os.getcwd(), "input", "udise", "section_shift.xlsx")
        try:
            data_parser = StudentDataParser(section_shift_data_file)
            data_parser.parse_data()
            self.student_data = StudentData(data_parser.get_parsed_data())
        except Exception as e:
            logger.error("Error preparing section shift data: %s", str(e))
            raise

    def start_section_shift(self):
        """
        Executes the UDISE Student Section Shift workflow.

        Workflow:
            1. Prepares section shift data.
            2. Opens the Section Shift UI option.
            3. Iterates through one or more classes provided in CLASSES.
            4. For each class:
                - Selects the class from the dropdown.
                - Determines the total number of pages.
                - Processes each page sequentially.
                - Navigates to the next page with a delay, if applicable.
            5. Exports the final section shift report.

        Notes:
            - If CLASSES is not a non-empty list, falls back to single-class selection.
            - Logs progress and warnings at each step for traceability.

        Raises:
            TimeoutException: If UI elements are not found or clickable within expected time.
            Exception: Propagates unexpected errors during workflow execution.
        """
        logger.info("Starting UDISE Student Section Shift workflow.")

        self._prepare_section_shift_data()
        ui = self.section_shift_ui

        multi_class_mode = isinstance(CLASSES, list) and bool(CLASSES)

        # Decide whether to select class immediately or defer until loop
        ui.select_section_shift_options(select_class=not multi_class_mode)

        # Log mode information
        if multi_class_mode:
            logger.info(
                "Multi-class mode enabled. Classes to process: %s", CLASSES)
        else:
            logger.info(
                "Single-class mode enabled. Using class from config: %s",
                CLASSES)

        logger.debug("Type of CLASSES : %s", type(CLASSES))
        logger.debug("Length of CLASSES : %s", len(CLASSES)
                     if isinstance(CLASSES, list) else "N/A")
        logger.debug("Class value from config : %s", CLASSES)

        for class_to_select in CLASSES:
            logger.info("Processing Class: %s", class_to_select)
            ui.select_section_shift_class(class_to_select)

            total_pages = ui.get_total_pages()
            if total_pages == 0:
                logger.warning(
                    "No pages found for section shift in class %s.", class_to_select)
                continue  # skip instead of returning, so other classes can still be processed

            for page in range(1, total_pages + 1):
                logger.info("Processing page %d of %d for class %s",
                            page, total_pages, class_to_select)
                self._process_section_shift_page()

                if page < total_pages:
                    logger.debug(
                        "Waiting for %s seconds before moving to next page", TIME_DELAY / 3)
                    time.sleep(TIME_DELAY / 3)
                    ui.go_to_next_page()

        self._export_section_shift_report()

    def _process_section_shift_page(self):
        """
        Process all student rows on the current Section Shift UI page.

        Iterates through the Section Shift table, attempts section shifts,
        and updates student data. Handles UI refreshes after successful shifts
        and exits once all students are processed.
        """
        ui = self.section_shift_ui
        processed = set()

        while True:
            student_rows = self._fetch_student_rows()
            if not student_rows:
                logger.warning("No students found on this page.")
                break

            logger.info("Total Students currently on this page: %d",
                        len(student_rows))
            progress_made = False

            for student_row in student_rows:
                if self._skip_student(student_row, processed):
                    continue

                student_pen, ui_section = ui.get_ui_student_pen_and_section(
                    student_row)
                status = self._process_single_student(
                    student_row, student_pen, ui_section)

                processed.add(student_pen)

                if "SUCCESS" in status.upper():
                    self.shifted_students.append(student_pen)
                    progress_made = True
                    break  # refresh immediately

            if not progress_made:
                break

    def _fetch_student_rows(self):
        """
        Retrieve the current list of student rows from the
        Section Shift UI table.

        Calls the UI helper to access the data table and
        returns all row elements for further processing.
        """
        ui = self.section_shift_ui
        return ui.get_section_shift_table_rows(
            ui.get_section_shift_data_table()
        )

    def _skip_student(self, student_row, processed):
        """
        Determine whether a student row should be skipped
        during section shift processing.

        A student is skipped if:
        * Their PEN is not found in the prepared data.
        * Their PEN has already been shifted in a previous iteration.
        * Their PEN has already been processed in the current pass.

        Args:
            student_row: The UI row element representing the student entry.
            processed (set): Collection of student PENs already handled in this pass.

        Returns:
            bool: True if the student should be skipped, False otherwise.
        """
        student_pen, _ = self.section_shift_ui.get_ui_student_pen_and_section(
            student_row)

        if not self._student_pen_exists(student_pen):
            logger.warning(
                "Student PEN %s not found in prepared data. Skipping.",
                student_pen)
            return True

        if student_pen in self.shifted_students or student_pen in processed:
            logger.info(
                "Student PEN %s already handled. Skipping.", student_pen)
            return True

        return False

    def _process_single_student(self, student_row, student_pen, ui_section):
        """
        Handle section shift processing for a single student row.

        This method:
        * Logs the student being processed.
        * Retrieves the student's prepared data and current section.
        * Attempts a section shift operation via the UI.
        * Updates the internal student data store with the outcome,
            including status, remarks, and section changes.
        * Waits briefly to respect UI timing before returning.

        Args:
            student_row: The UI row element representing the student entry.
            student_pen (str): Unique PEN identifier for the student.
            ui_section (str): Section value retrieved from the UI for
                                the student.

        Returns:
            str: The status message from the section shift attempt
                (e.g., "SUCCESS", "Already Matched", "Skipped").
        """

        logger.info("Processing Student PEN: %s", student_pen)

        student_data = self.student_data.get_student_data().get(student_pen)
        student = Student(student_pen, student_data)
        student_section = student.get_section()

        status, section_shift_status = self._handle_section_shift(
            student_pen, ui_section, student_section, student_row
        )

        logger.info("%s: Section Shift Status: %s", student_pen, status)
        self.student_data.update_student_data(
            student_pen,
            {
                "Section Shift Status": section_shift_status,
                "Remark": status,
                "Old Section": ui_section,
                "Updated Section": student_section,
            },
        )

        self._wait_between_students()
        return status

    def _handle_section_shift(self, student_pen, ui_section,
                              student_section, student_row):
        """
        Handle the section shift logic for a single student row.

        This method compares the section value from the UI with the section
        value from prepared student data. If a mismatch is detected, it
        triggers a section shift operation in the UI and retrieves the
        resulting status message. Otherwise, it returns a message indicating
        that the section is already matched.

        Args:
            student_pen (str): The PEN number of the student being processed.
            ui_section (str): The section value retrieved from the UI table.
            student_section (str): The section value from prepared student data.
            student_row (WebElement): The table row element corresponding to the student.

        Returns:
            tuple[str, str]: A tuple containing:
                - status (str): The message describing the result of the section shift.
                - section_shift_status (str): "Yes" if the section shift was successful
                or already matched, "No" otherwise.
        """
        ui = self.section_shift_ui
        if self._is_section_mismatch(ui_section, student_section):
            logger.info(
                "%s: Section Mismatch, UDISE Section-%s, Student Section-%s",
                student_pen,
                ui_section,
                student_section,
            )
            ui.shift_section(student_pen, student_section, student_row)
            status = ui.get_section_shift_message()
            return status, "Yes" if "Successfully" in status else "No"
        return "Section Matched Already", "Yes"

    def _student_pen_exists(self, student_pen):
        """
        Check whether the given student PEN exists
        in the prepared student data.

        Args:
            student_pen (str): The PEN number of the student to check.

        Returns:
            bool: True if the PEN is present in the student data,
                    False otherwise.
        """
        return student_pen in self.student_data.get_student_data()

    def _wait_between_students(self):
        """Helper to log and wait between student processing."""
        logger.debug("Waiting for %s seconds", TIME_DELAY / 3)
        time.sleep(TIME_DELAY / 3)

    def _is_section_mismatch(self, ui_section, student_section):
        """
        Checks if there is a mismatch between UI section and
        student data section.

        Args:
            ui_section (str): The section value retrieved from the UI.
            student_section (str): The section value from the student data.
        Returns:
            True if there is a mismatch, False otherwise.
        """
        return ui_section != student_section

    def _export_section_shift_report(self):
        """
        Exports the section shift report to an Excel file.

        This method utilizes the ReportExporter utility to generate
        an Excel report containing the section shift results for all
        processed students.

        Returns:
            None
        """
        try:
            ReportExporter(self.student_data.get_student_data(),
                           report_sub_dir="udise",
                           filename="student_section_shift_report"
                           ).save(first_column="Student PEN Number")
            logger.info("Section shift report exported successfully.")
        except Exception as e:
            logger.error("Error exporting section shift report: %s", str(e))
            raise
