"""
Automates the UDISE Student Section Shift workflow using Selenium.

This module handles UI interactions required to initiate
Student Section Shift task and execute section shifting task within the
UDISE portal Student Module. It leverages modular UI components and centralized
configuration.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-12-09
Last Modified: 2026-01-13

Version: 1.0.0
"""

import os
import time

from common.config import TIME_DELAY
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
        Initiates the Student Section Shift workflow.

        This method launches the browser, logs into the UDISE portal,
        navigates to the section shift module, and performs the section
        shifting task.

        Returns:
            None
        """
        logger.info("Starting UDISE Student Section Shift workflow.")

        self._prepare_section_shift_data()
        ui = self.section_shift_ui
        ui.select_section_shift_options()

        total_pages = ui.get_total_pages()
        if total_pages == 0:
            logger.warning("No pages found for section shift.")
            return

        for page in range(1, total_pages + 1):
            logger.info("Processing page %d of %d", page, total_pages)
            self._process_section_shift_page()

            if page < total_pages:
                logger.debug("Waiting for %s seconds", TIME_DELAY)
                time.sleep(TIME_DELAY)
                ui.go_to_next_page()
        self._export_section_shift_report()

    def _process_section_shift_page(self):
        """
        Processes a single page of the Section Shift table.

        This method iterates through each student entry on the current
        page, retrieves the necessary data, and performs the section shift
        operation based on the prepared student data.

        Returns:
            None
        """
        ui = self.section_shift_ui
        student_rows = ui.get_section_shift_table_rows(
            ui.get_section_shift_data_table())

        students_count = len(student_rows)
        if students_count == 0:
            logger.warning("No students found on this page.")
            return

        logger.info("Total Students on this page: %d", students_count)

        for index, student_row in enumerate(student_rows, start=1):
            logger.info("Processing  [%d/%d] Student", index, students_count)

            student_pen, ui_section = ui.get_ui_student_pen_and_section(
                student_row)

            logger.info("Processing Student PEN: %s", student_pen)

            student = Student(
                student_pen, self.student_data.get_student_data().get(student_pen))
            student_section = student.get_section()

            if self._is_section_mismatch(ui_section, student_section):
                logger.info(
                    "%s: Section Mismatch, UDISE Section-%s, "
                    "Student Section-%s",
                    student_pen,
                    ui_section,
                    student_section,
                )
                ui.shift_section(student_pen, student_section, student_row)
                status = ui.get_section_shift_message()
                section_shift_status = "Yes" if "Successfully" in status else "No"
            else:
                status = "Section Matched Already"
                section_shift_status = "Yes"

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

    def _wait_between_students(self):
        """Helper to log and wait between student processing."""
        logger.debug("Waiting for %s seconds", TIME_DELAY)
        time.sleep(TIME_DELAY)

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
