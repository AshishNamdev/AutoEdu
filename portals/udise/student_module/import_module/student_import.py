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
Last Modified: 2025-09-18

Version: 1.0.0
"""

from common.config import PASSWORD, USERNAME
from common.logger import logger
from common.time_utils import get_timestamp
from portals.udise import Student
from portals.udise.student_module.release_request import ReleaseRequest
from ui.udise.login import StudentLogin
from ui.udise.student_import import StudentImportUI
from utils.parser import StudentImportDataParser
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

    def __init__(self):
        """
        Initialize the StudentImport controller.

        Performs login to the UDISE portal using credentials from config,
        and sets up the UI handler for import operations.
        """
        login = StudentLogin()
        login.student_login(USERNAME, PASSWORD, max_attempts=3)
        self.logged_in_school = login.get_logged_in_school()
        self.import_ui = StudentImportUI()
        self.student = None
        self.import_data = self.prepare_import_data()
        self.relase_request = {}
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

    def prepare_import_data(self):
        """
        Prepares and retrieves student import data.

        This method initializes a StudentImportDataParser instance,
        parses the input data, and returns the structured import data
        ready for further processing or storage.

        Returns:
            dict: A dictionary containing parsed student import data.
        """
        data_parser = StudentImportDataParser()
        data_parser.parse_data()
        return data_parser.get_import_data()

    def init_student_import(self):
        """
        Initiate the student import workflow.

        Triggers UI interactions to select import options and
        prepare the portal for data ingestion.
        This method serves as the entry point for the import process.
        """
        self.import_ui.select_import_options()
        self._import_students()
        ReportExporter(self.import_data, report_sub_dir="udise",
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
        for pen_no, student_data in self.import_data.items():
            if self._is_invalid_pen_no(pen_no):
                continue

            student = Student(pen_no, student_data)
            status = self._try_import_student(pen_no, student)

            if status == "active":
                if self._is_school_matched(pen_no):
                    continue
                self.raise_release_request(pen_no, self.pen_dob)
            elif self._is_import_error(pen_no, status):
                continue
            elif self._is_class_mismatch(pen_no, student.get_class()):
                continue
            else:
                ui.submit_import_data(
                    student.get_class(),
                    student.get_section(),
                    student.get_admission_date()
                )
                status = str(ui.get_import_message()).strip()
                logger.info("%s : %s", pen_no, status)
                self._update_import_data(
                    pen_no, {"Remark": status, "Import Status": "Yes"})

    def _try_import_student(self, pen_no, student):
        """
        Attempts to import a student using PEN no. and Aadhaar DOB.
        Updates remark in import_data if Aadhaar DOB is missing.

        - If a DOB mismatch occurs, retries using Aadhaar DOB.
        - Determines the student's status via UI feedback.

        Returns:
            status (str): Final status after import attempt.
        """
        # Rest PEN DOB to None
        self.pen_dob = None
        ui = self.import_ui
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
                    self._update_import_data(pen_no, {
                        "Remark": "Aadhaar DOB missing",
                        "Import Status": "No"
                    })
                    logger.warning("%s - Aadhaar DOB missing", pen_no)
                    return "aadhaar_dob_missing"

                # Skip retry if Aadhaar DOB is same as PEN DOB
                if source == "PEN" and dob_attempts[1][1] == dob:
                    logger.warning(
                        "%s - Aadhaar DOB matches PEN DOB — skipping retry",
                        pen_no)
                    return "dob_retry_skipped"
            else:
                # Set PEN DOB to working DOB
                self.pen_dob = dob
                status = ui.get_student_status()
                logger.info("%s : %s", pen_no, status)
                return status
        return "dob_error"

    def _is_school_matched(self, pen_no):
        """
        Determines whether the student's current school matches the
        logged-in school.

        Retrieves the student's current school from the UI and compares it with
        the logged-in school (`self.logged_in_school`). If they match
        (case-insensitive), logs an informational message and updates the
        import status as "Already Imported". If they differ,
        logs a warning but does not update the import status.

        Args:
            pen_no (str): The student's PEN number used for logging
                            and data update.

        Returns:
            bool: True if the current school matches the logged-in school,
                False if a mismatch is detected.
        """

        current_school = self.import_ui.get_student_current_school().strip()
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

    def _update_import_data(self, pen_no, kwargs):
        """
        Updates the import data for a specific student identified
        by PEN number.

        This method modifies the `import_data` dictionary by setting the
        specified `key` to the provided `value` for the student with the
        given `pen_no`. If the `pen_no` does not exist in the dictionary,
        it logs a warning message.

        Args:
            pen_no (str): The PEN number of the student whose data
                            is to be updated.
            kwargs (dict): The key and value to add in  student's
                            data dictionary.

        Returns:
            None

        Side Effects:
            - Modifies the `import_data` attribute of the class instance.
            - Logs a warning if the specified PEN number is not found.
        """
        if pen_no in self.import_data:
            for key, value in kwargs.items():
                self.import_data[pen_no][key] = value
                logger.debug("Updated %s: %s - %s", pen_no, key, value)
            self.import_data[pen_no]["Date and Time"] = get_timestamp(
                format="%d-%m-%Y - %I:%M:%S %p")
        else:
            logger.warning("%s not found in import data. No update made.",
                           pen_no)

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
            self._update_import_data(
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
        self._update_import_data(
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
                self._update_import_data(
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
            self._update_import_data(
                pen_no,
                {
                    "Remark": match_remark,
                    "Import Status": "Yes"
                }
            )
        return False

    def raise_release_request(self, pen_no, dob):

        release_request = ReleaseRequest(pen_no, dob)
