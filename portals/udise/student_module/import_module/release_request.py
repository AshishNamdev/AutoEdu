"""
Release Request workflow orchestrator for UDISE Student Module.

This module coordinates the release request process for a batch of students
using the UDISE UI automation layer. It delegates UI interactions to
`ReleaseRequestUI` and manages student-specific data flow.

Usage:
    - Instantiate `ReleaseRequest` with a list of student objects.
    - Call `start_release_request()` to initiate the release request flow.

Includes:
    - UI navigation and form filling for release requests
    - Student data extraction and submission coordination

Author: Ashish Namdev(ashish28[at] sirt[dot] gmail[dot] com)

Date Created:  2025-09-14
Last Modified: 2025-10-03

Version: 1.0.0
"""

from common.logger import logger
from ui.udise.release_request_ui import ReleaseRequestUI


class ReleaseRequest:
    """
    Orchestrates the release request process for a batch of students.

    This class manages the end-to-end flow of generating release requests
    by interacting with the UDISE UI and student data objects.

    Attributes:
    -----------
    students : list
        A list of student objects containing PEN and DOB information.

    ui : ReleaseRequestUI
        UI handler for interacting with the release request interface.

    Usage:
        release_request = ReleaseRequest(students)
        release_request.start_release_request()

    Includes:
        - Option selection and form filling via UI
        - Student data extraction and logging
        - Hooks for future submission and post-processing
    """

    def __init__(self, students, student_data):
        """
        Initializes the ReleaseRequest object with a list
        of students and a student's data record.

        Args:
            students (list): A list of student objects or data to be processed.
            student_data (object): An instance of StudentData.
        """
        self.students = students
        self.student_data = student_data
        self.ui = ReleaseRequestUI()

    def start_release_request(self):
        """
        Initiates the release request workflow.

        Steps:
        - Navigates through the release request UI options.
        - Calls internal method to generate requests for each student.

        Raises:
            TimeoutException: If UI elements are not interactable.
        """
        logger.info("Total release requests to be raised: %d",
                    len(self.students))
        self.ui.select_release_request_options()
        self._generate_release_request()

    def _generate_release_request(self):
        """
        Generates and submits release requests for each student in the list.
        For each student, this method:
        - Retrieves the PEN (Permanent Enrollment Number) and date of birth.
        - Initiates the release request process via the UI.
        - Checks if the student's name is available; logs a warning and skips
            if not found.
        - Logs the processing details for the student.
        - Submits the release request data including section and
            admission date.
        - Retrieves and logs the status of the release request.
        - Updates the parsed data with the release request status and
            marks the import status as "Yes".
        Logs relevant information and warnings throughout the process.
        """

        ui = self.ui
        for student in self.students:
            pen_no = student.get_student_pen()
            dob = student.get_pen_dob()
            ui.generate_release_request(pen_no, dob)
            student_name = ui.get_ui_student_name()

            if "na" == student_name.casefold():
                logger.warning(
                    "Student name not found for PEN: %s, "
                    "Skipping student", pen_no)
                continue

            logger.info("Processing Release Request for: %s, PEN: %s, DOB: %s",
                        student_name, pen_no, dob)
            ui.submit_release_request_data(
                student.get_section(), student.get_admission_date())
            status = str(ui.get_release_request_status()).strip()
            logger.info(
                "%s : Student's Current School: %s : Release Request Status: %s",
                pen_no,
                student.get_current_school(),
                status
            )

            self.student_data.update_student_data(
                pen_no, {"Remark": status, "Import Status": "No"})
