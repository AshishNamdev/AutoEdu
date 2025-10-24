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

Date Created:  2025-08-20
Last Modified: 2025-10-24

Version: 1.0.0
"""

import os
import re

from common.logger import logger
from common.student_data import StudentData
from portals.udise import ReleaseRequest, SearchPEN, Student
from ui.udise.student_import_ui import StudentImportUI
from utils.parser import StudentDataParser
from utils.report import ReportExporter


class StudentImport:
    """
    Controller class for automating student import tasks in the UDISE portal.

    This class handles login authentication and delegates UI interactions to
    the `StudentImportUI` component. Designed for modular expansion to support
    additional import workflows and error handling.

    Attributes:
        import_ui (StudentImportUI): UI handler for student import
                                    interactions.
    """

    def __init__(self, logged_in_school):
        """
        Initialize the StudentImport controller.

        Performs login to the UDISE portal using credentials from config,
        and sets up the UI handler for import operations.
        """
        self.logged_in_school = logged_in_school
        self.import_ui = StudentImportUI()
        self.student = None
        self.release_requests = []
        self.import_errors = {
            "dob_error": (
                "The entered Date of Birth(DOB) does not match "
                "with the respective Student PEN"
            ),
            "aadhaar_dob_missing": "Aadhaar DOB missing",
            "dob_retry_skipped": (
                "Retry with Aadhaar DOB skipped as it matches PEN DOB"
            ),
            "unknown": (
                "Unexpected error during import — "
                "may involve Selenium timeouts, UI "
                "failures, or system-level issues."
            )
        }
        self.pen_dob = None
        self.student_data = None
        self.dob_errors = [
            key for key in self.import_errors if "dob" in key]
        self.dob_error_students = {}

    def _prepare_import_data(self):
        """
        Prepares and retrieves student import data.

        This method initializes a StudentImportDataParser instance,
        parses the input data, and returns the structured import data
        ready for further processing or storage.

        Returns:
            dict: A dictionary containing parsed student import data.
        """
        import_data_file = os.path.join(
            os.getcwd(), "input", "udise", "import_data.xlsx")
        data_parser = StudentDataParser(import_data_file)
        data_parser.parse_data()
        self.student_data = StudentData(data_parser.get_parsed_data())

    def start_student_import(self):
        """
        Start the student import workflow.

        Triggers UI interactions to select import options and
        prepare the portal for data ingestion.
        This method serves as the entry point for the import process.
        """
        self.import_ui.select_import_options()
        self._prepare_import_data()
        total_students = len(self.student_data.get_student_data())
        logger.info(
            "[UDISEImport] Starting student import: %s records to process",
            total_students
        )

        try:
            self._import_students()

            # Try reimport students with DOB Error
            if self.dob_error_students:
                logger.info("retrying import for students: %s",
                            self.dob_error_students.keys())
                self._import_students()

            if self.release_requests:
                ReleaseRequest(self.release_requests,
                               self.student_data).start_release_request()
        except Exception as e:
            logger.exception(
                "UDISE Student Import encountered an error: %s", str(e))
        finally:
            logger.info(
                "[UDISEImport] Student import completed: "
                "%s records successfully processed",
                total_students
            )

            ReportExporter(self.student_data.get_student_data(),
                           report_sub_dir="udise",
                           filename="student_import_report"
                           ).save(first_column="Student PEN Number")

    def _import_students(self):
        """
        Imports a batch of students by validating their DOB and determining
        import eligibility.

        For each student:
        - Attempts import using the primary DOB.
        - If the student is already active elsewhere,
            check if it's in current logged in school else
            raie the release request.
        - Otherwise, fills in import details such as class, section,
            and admission date and submits the import form.

        Side Effects:
            - Logs status messages for each student.
            - Triggers UI operations for import, release, or detail filling.
        """
        logger.info("Starting Student Import workflow")
        ui = self.import_ui
        student_data_dict = self.student_data.get_student_data()
        use_dob_errors = bool(self.dob_error_students)

        # Unified source of PENs
        pen_numbers = (
            self.dob_error_students.keys()
            if use_dob_errors else student_data_dict.keys()
        )

        for pen_no in pen_numbers:
            self.pen_dob = None

            student = (
                self.dob_error_students.get(pen_no)
                if use_dob_errors else Student(pen_no, student_data_dict.get(pen_no))
            )

            if self._is_invalid_pen_no(pen_no):
                self.search_pen_and_dob(student)
                if student.get_searched_pen_no() is None:
                    continue

            status = self._try_import_student(student)
            logger.info("status after import attempt: %s", status)
            student.set_pen_dob(self.pen_dob)
            current_school = self.logged_in_school

            if status == "active":
                current_school = ui.get_student_current_school().strip()
                student.set_current_school(current_school)

                if self._is_school_matched(pen_no, current_school):
                    continue

                self._prepare_release_request(student)

            elif self._is_dob_error(pen_no, status):
                # Handle DOB mismatch by re-searching PEN and DOB
                self.search_pen_and_dob(student)
                self.dob_error_students.update({pen_no: student})

            elif self._is_import_error(pen_no, status):
                continue

            elif self._is_class_mismatch(pen_no, student.get_class()):
                continue

            else:
                current_school = ui.get_student_current_school().strip()
                ui.submit_import_data(
                    student.get_class(),
                    student.get_section(),
                    student.get_admission_date()
                )
                status = str(ui.get_import_message()).strip()
                logger.info("%s : %s", pen_no, status)
                self.student_data.update_student_data(
                    pen_no, {"Remark": status, "Import Status": "Yes"})

            student.set_current_school(current_school)
            logger.info("Processing next student for import")

    def _try_import_student(self, student):
        """
        Attempts to import a student record using their PEN number and date of
        birth (DOB), handling both PEN and Aadhaar DOB sources.

        The function follows this workflow:
            1. Attempts import using the PEN DOB.
            2. If the DOB does not match, retries using the Aadhaar DOB
               (if available).
            3. Handles cases where Aadhaar DOB is missing or identical to
               PEN DOB, updating import data with appropriate remarks.
            4. Logs errors and warnings for mismatches and missing data.
            5. Returns the final status from the UI after the import attempt.

        Args:
            student (Student): The student object containing PEN number and
                DOB information.

        Returns:
            str: The final status after the import attempt. Possible values
                include:
                - "active": Import successful.
                - "dob_error": DOB mismatch after all attempts.
                - "aadhaar_dob_missing": Aadhaar DOB not available.
                - "dob_retry_skipped": Retry skipped due to identical DOBs.
                - Other error codes as returned by the UI.
        """
        logger.info("Attempting import for current student record")
        ui = self.import_ui
        pen_no = student.get_student_pen()
        searhced_pen_no = student.get_searched_pen_no()
        pen_no = searhced_pen_no if searhced_pen_no else pen_no

        if searhced_pen_no is None:
            dob_attempts = [
                ("PEN", student.get_dob()),
                ("Aadhaar", student.get_adhaar_dob())
            ]
        else:
            dob_attempts = [("PEN", student.get_pen_dob())]

        for source, dob in dob_attempts:
            if source == "Aadhaar" and dob is None:
                logger.info("Aadhaar DOB Missing")
                return "aadhaar_dob_missing"

            ui.import_student(pen_no, dob)
            if ui.get_pen_status() == "dob_error":
                status = ui.get_ui_dob_status()

                logger.error("%s - %s: %s", pen_no, dob, status)
                logger.debug("source = %s, dob = %s", source, dob)

                # Skip retry if Aadhaar DOB is same as PEN DOB
                if (
                    source == "PEN"
                    and str(dob_attempts[1][1]).strip() == str(dob).strip()
                ):
                    logger.info("Aadhaar DOB is same as PEN DOB")
                    return "dob_retry_skipped"

            else:
                # Set PEN DOB to working DOB
                self.pen_dob = dob
                status = ui.get_student_status()
                logger.info("%s : %s", pen_no, status)
                self.student_data.update_student_data(
                    student.get_student_pen(), {"PEN DOB": self.pen_dob})
                return status
        return "dob_error"

    def _is_school_matched(self, pen_no, current_school):
        """
        Determines if the student's current school matches the logged-in
        school.

        Compares the provided `current_school` value with
        `self.logged_in_school` (case-insensitive). If they match, logs an
        informational message and updates the import status as
        "Already Imported". If they do not match, logs a warning but does
        not update the import status.

        Args:
            pen_no (str): The student's PEN number, used for logging and
                data update.
            current_school (str): The name of the student's current school.

        Returns:
            bool: True if the current school matches the logged-in school,
                False otherwise.
        """

        logged_in_school = self.logged_in_school.strip()

        return not self._handle_field_validation(
            "School", pen_no,
            logged_in_school, current_school,
            update_on_match=True, match_remark="Already Imported",
            update_on_mismatch=False  # Don't update if mismatch
        )

    def _is_class_mismatch(self, pen_no, student_class):
        """
        Checks whether the student's class mismatches the import UI class.

        Compares the provided `student_class` with the class retrieved from the
        import UI. If they differ (case-insensitive), logs a warning and
        updates the import status with a mismatch remark.
        If they match, no update occurs.

        Args:
            pen_no (str): The student's PEN number used for logging and
                            data update.
            student_class (str): The class value associated with the
                            student record.

        Returns:
            bool: True if a class mismatch is detected and handled,
                    False otherwise.
        """

        return self._handle_field_validation(
            "Class",
            pen_no,
            student_class,
            self.import_ui.get_import_class(),
            update_on_match=False,
            update_on_mismatch=True
        )

    def _is_invalid_pen_no(self, pen_no):
        """
        Returns True if the PEN number is invalid.
        Criteria:
        - Must be a non-empty string of digits
        - Length must be between 11 and 14 characters
        - Must not contain any alphabetic characters or known placeholders
        """
        if not pen_no:
            return True

        pen_no = str(pen_no).strip().upper()

        # Known invalid placeholders
        invalid_placeholders = {"NA", "NS", "N/A", "NULL", "NONE", ""}

        if pen_no in invalid_placeholders:
            return True

        # Regex: only digits, length 11 to 14
        return not re.fullmatch(r"\d{11,14}", pen_no)

    def _is_import_error(self, pen_no, status):
        """
        Checks whether the given import status indicates an error condition.

        If the status exists in the `self.import_errors` dictionary,
        logs a warning, updates the import data with a remark and sets
        the importstatus to "No".

        Args:
            pen_no (str): The student's PEN number used for logging
                            and data update.
            status (str): The import status to validate against known
                            error conditions.

        Returns:
            bool: True if the status is recognized as an import error,
                    False otherwise.
        """
        error_remark = self.import_errors.get(status)
        if not error_remark:
            return False

        logger.warning(
            "%s : Skipping import due to %s issues",
            pen_no,
            error_remark,
        )
        self.student_data.update_student_data(
            pen_no,
            {
                "Remark": error_remark,
                "Import Status": "No"
            }
        )
        return True

    def _is_dob_error(self, pen_no, status):
        """
        Checks whether the given import status indicates an
        DOB error condition.

        If the dob  exists in the `self.import_errors` dictionary keys
        logs a warning, updates the import data with a remark and sets
        the import status to "No".

        Args:
            pen_no (str): The student's PEN number used for logging
                            and data update.
            status (str): The import status to validate against known
                            dob error conditions.

        Returns:
            bool: True if the status is recognized as an dob error,
                    False otherwise.
        """
        if status not in self.dob_errors:
            return False

        error_msg = "DOB Error in Student Import (dob_error/aadhaar_dob_missing)"
        logger.warning(
            "%s : Skipping import due to %s issues", pen_no, error_msg)
        self.student_data.update_student_data(
            pen_no,
            {
                "Remark": error_msg,
                "Import Status": "No"
            }
        )
        return True

    def _handle_field_validation(
        self,
        field_name,
        pen_no,
        expected_value,
        actual_value,
        update_on_match=False,
        update_on_mismatch=True,
        match_remark="Already Imported"
    ):
        """
        Validates a field by comparing expected and actual values
        (case-insensitive), logs the result, and conditionally
        updates import data.

        Args:
            field_name (str): Name of the field being validated.
            pen_no (str): Student's PEN number.
            expected_value (str): Expected value from student record.
            actual_value (str): Actual value from UI or import source.
            update_on_match (bool): Whether to update import data on match.
            update_on_mismatch (bool): Whether to update import data on
                                       mismatch.
            match_remark (str): Remark to use when values match.

        Returns:
            bool: True if mismatch detected, False otherwise.
        """
        expected = str(expected_value).strip()
        actual = str(actual_value).strip()

        if expected.casefold() != actual.casefold():
            logger.warning(
                "%s : %s mismatch. Expected: %s, Actual: %s",
                pen_no,
                field_name,
                expected,
                actual,
            )
            if update_on_mismatch:
                remark = (
                    f"{field_name} Mismatch :\n"
                    f"  Expected - {expected}\n"
                    f"  Actual   - {actual}"
                )
                self.student_data.update_student_data(
                    pen_no,
                    {
                        "Remark": remark,
                        "Import Status": "No"
                    }
                )
            return True

        logger.info(
            "%s : %s match confirmed. Expected: %s, Actual: %s",
            pen_no,
            field_name,
            expected,
            actual,
        )
        if update_on_match:
            self.student_data.update_student_data(
                pen_no,
                {
                    "Remark": match_remark,
                    "Import Status": "Yes"
                }
            )
        return False

    def _prepare_release_request(self, student):
        """
        Prepares a release request entry for a student.

        Appends student object to the `self.release_request` list
        for later processing or export.

        Args:
            student (Student): The student object containing PEN number
                               and DOB information.
        """
        self.release_requests.append(student)
        pen_no = student.get_student_pen()
        logger.debug(
            "%s: Student already active in another school: %s, "
            "preparing release request data",
            pen_no,
            student.get_current_school()
        )
        self.student_data.update_student_data(
            pen_no,
            {
                "Remark": "Active in another school",
                "Import Status": "No"
            }
        )

    def search_pen_and_dob(self, student):
        """
        Perform PEN and DOB lookup for the given student using
        fallback strategies.

        Workflow:
        1. Instantiate a SearchPEN handler for the student.
        2. Execute the PEN + DOB search on UDISE UI.
        3. Retrieve and store the resolved PEN in student.

        Args:
            student (Student): The student object to process.

        """
        logger.info("Searching PEN and DOB for adhaar number %s",
                    student.get_adhaar_number())
        searcher = SearchPEN(student, self.student_data)
        searcher.search_pen_and_dob()

        pen_no = searcher.get_pen_no()
        pen_dob = searcher.get_dob()

        if pen_no is None:
            logger.error(
                "PEN not found for Aadhaar number: %s",
                student.get_adhaar_number()
            )
            self.student_data.update_student_data(
                student.get_student_pen(),
                {
                    "Remark": "PEN not found using Aadhaar",
                    "Import Status": "No"
                }
            )
        else:
            student.set_searched_pen_no(pen_no)
            student.set_pen_dob(pen_dob)
