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
Last Modified: 2025-10-03

Version: 1.0.0
"""

import os

from common.logger import logger
from common.student_data import StudentData
from portals.udise import ReleaseRequest, Student
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
            )
        }
        self.pen_dob = None
        self.student_data = None

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
        self._import_students()
        if self.release_requests:
            ReleaseRequest(self.release_requests,
                           self.student_data).start_release_request()

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
        ui = self.import_ui
        for pen_no, student_data in self.student_data.get_student_data().items():
            self.pen_dob = None
            if self._is_invalid_pen_no(pen_no):
                continue

            student = Student(pen_no, student_data)
            status = self._try_import_student(student)
            student.set_pen_dob(self.pen_dob)
            current_school = self.logged_in_school

            if status == "active":
                current_school = ui.get_student_current_school().strip()
                student.set_current_school(current_school)

                if self._is_school_matched(pen_no, current_school):
                    continue

                self._prepare_release_request(student)
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
        ui = self.import_ui
        pen_no = student.get_student_pen()
        dob_attempts = [
            ("PEN", student.get_dob()),
            ("Aadhaar", student.get_adhaar_dob())
        ]

        for source, dob in dob_attempts:
            ui.import_student(pen_no, dob)
            if ui.get_pen_status() == "dob_error":
                status = ui.get_ui_dob_status()
                logger.error("%s - %s: %s", pen_no, dob, status)

                if dob is None and source == "Aadhaar":
                    return "aadhaar_dob_missing"

                # Skip retry if Aadhaar DOB is same as PEN DOB
                if source == "PEN" and dob_attempts[1][1] == dob:
                    return "dob_retry_skipped"
            else:
                # Set PEN DOB to working DOB
                self.pen_dob = dob
                status = ui.get_student_status()
                logger.info("%s : %s", pen_no, status)
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
        Determines if the given PEN number is invalid.

        A PEN number is considered invalid if it contains the substring
        "na" (case-insensitive).
        If invalid, logs an error and updates the import data with a remark
        and status.

        Args:
            pen_no (str): The PEN number to validate.

        Returns:
            bool: True if the PEN number is invalid, False otherwise.
        """
        if "na" in pen_no.lower():
            logger.error("Skipping invalid PEN no.: %s", pen_no)
            self.student_data.update_student_data(
                pen_no,
                {
                    "Remark": "Invalid PEN no.",
                    "Import Status": "No"
                }
            )
            return True
        return False

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
