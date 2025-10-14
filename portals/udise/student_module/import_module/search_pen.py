"""
Purpose:
    Provides a robust fallback mechanism to retrieve a student's
    PEN (Permanent Education Number) and date of birth (DOB) using
    Aadhaar number and inferred Year of Birth (YOB) trials.

Overview:
    This module is designed for UDISE student import workflows where
    PEN and DOB may be missing or inconsistent.
    It uses a multi-layered strategy to recover these values by interacting
    with the Search PEN UI.

Fallback Strategy:
    1. Direct YOB from Aadhaar DOB or student DOB.
    2. YOB trial range ±MAX_YOB_TRIAL_RANGE from known DOBs.
    3. Inferred YOB from student class using CLASS_AGE_MAP
        if DOBs are unavailable.

Key Components:
    - SearchPEN class: Encapsulates PEN search logic and student state.
    - CLASS_AGE_MAP: Maps class levels to expected student age
        for YOB inference.
    - MAX_YOB_TRIAL_RANGE: Controls the range of YOB trials around base year.
    - CURRENT_YEAR: Used for class-based YOB inference.

Dependencies:
    - Selenium-based SearchPENUI for UI automation.
    - get_year_from_date utility for extracting year from date strings.
    - Structured logging via common.logger.

Usage:
    Instantiate SearchPEN with a student object and student_data handler.
    Call `search_pen()` to attempt PEN and DOB retrieval.
    Access results via `get_pen_no()`, `get_dob()`, and `get_error_message()`.

Example:
    searcher = SearchPEN(student, student_data)
    searcher.search_pen()
    pen = searcher.get_pen_no()
    dob = searcher.get_dob()

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-10-10
Last Modified: 2025-10-14

Version: 1.0.0
"""

from datetime import datetime

from common.logger import logger
from ui.udise.search_pen_ui import SearchPENUI
from utils.date_time_utils import get_year_from_date

CLASS_AGE_MAP = {
    "1": 6, "2": 7, "3": 8, "4": 9, "5": 10,
    "6": 11, "7": 12, "8": 13, "9": 14, "10": 15,
    "11": 16, "12": 17
}

MAX_YOB_TRIAL_RANGE = 3
CURRENT_YEAR = datetime.now().year


class SearchPEN:
    """
    Handles the retrieval of a student's PEN (Permanent Education Number) and
    date of birth (DOB) using Aadhaar number and fallback Year of Birth
    (YOB) strategies.

    This class is part of the UDISE student import pipeline and is responsible
    for:
    - Validating Aadhaar presence
    - Preparing candidate YOBs using student DOB, Aadhaar DOB, or class-based
        inference
    - Interacting with the Search PEN UI to retrieve PEN and DOB
    - Logging and updating student records with results or errors

    Attributes:
        student (Student): The student object containing Aadhaar, DOB, class,
                            and PEN metadata.
        student_data (StudentData): Handler for updating student records
                                    post-search.
        pen_no (str | None): Retrieved PEN number, if found.
        dob (str | None): Retrieved or inferred date of birth, if found.
        error_message (str | None): Error message encountered during search,
                                    if any.

    Usage:
        searcher = SearchPEN(student, student_data)
        searcher.search_pen()
        pen = searcher.get_pen_no()
        dob = searcher.get_dob()
    """

    def __init__(self, student, student_data):
        """
        Initialize the SearchPEN instance with student context and data handler.

        Args:
            student (Student): The student object containing Aadhaar, DOB, class, and PEN metadata.
            student_data (StudentData): The data handler used to update student records post-search.

        Attributes:
            pen_no (str | None): Retrieved PEN number after search, if found.
            dob (str | None): Retrieved or inferred date of birth, if found.
            error_message (str | None): Error message encountered during search, if any.
        """
        self.student = student
        self.student_data = student_data
        self.pen_no = None
        self.dob = None
        self.error_message = None

    def get_pen_no(self):
        """
        Retrieve the student's PEN (Permanent Education Number).

        Returns:
            str: The PEN associated with the student.
        """
        return self.pen_no

    def get_dob(self):
        """
        Retrieve the student's date of birth.

        Returns:
            str: The student's DOB in 'YYYY-MM-DD' format.
        """
        return self.dob

    def get_error_message(self):
        """
        Retrieve any error message encountered during the PEN search.

        Returns:
            str: Error message if any, otherwise None.
        """
        return self.error_message

    def search_pen_and_dob(self):
        """
        Attempt to retrieve the student's PEN and DOB using Aadhaar number and
        YOB trials.

        Workflow:
        1. Validate Aadhaar number.
        2. Prepare candidate Year of Birth (YOB) values using fallback logic.
        3. For each YOB:
            - Set birth year in Search UI.
            - Trigger PEN + DOB search.
            - If successful, store retrieved PEN and DOB.
        4. If no result is found, student remains unprocessed.

        Updates:
            - On Aadhaar missing: logs error and marks student as unimportable.
            - On successful search: updates internal PEN and DOB attributes.

        Raises:
            TimeoutException: If UI elements are not interactable
                                during search.
        """
        # Step 1: Validate Aadhaar number
        aadhaar_no = self.student.get_adhaar_number()
        pen_no = self.student.get_student_pen()

        if aadhaar_no is None:
            logger.error(
                "Missing Aadhaar number for %s. Skipping student.", pen_no)
            self.error_message = "Missing Aadhaar number"
            self.student_data.update_student_data(
                pen_no,
                {"Error": self.error_message, "Import Status": "No"}
            )
            return

        # Step 2: Initialize search UI and prepare YOB trials
        ui = SearchPENUI(aadhaar_no)
        yob_trial = self._prepare_yob_trials()

        # Step 3: Attempt PEN search for each YOB
        for yob in yob_trial:
            ui.set_birth_year(yob)
            ui.search_ui_pen_and_dob()

            if ui.get_search_status() == "ok":
                self.pen_no = ui.get_pen_no()
                self.dob = ui.get_dob()
                logger.info("PEN found for aadhaar %s: (PEN: %s) (DOB: %s)",
                            aadhaar_no, self.pen_no, self.dob)
                self.student_data.update_student_data(
                    pen_no,
                    {"Searched PEN": self.pen_no, "PEN DOB": self.dob}
                )
                break
        else:
            logger.warning(
                "No PEN found for aadhaar number %s after YOB trials: %s",
                aadhaar_no,
                yob_trial
            )

    def _get_birth_year_from_dob(self):
        """
        Extract the birth year from the student's official DOB.

        Returns:
            int | None: Birth year if DOB is valid, otherwise None.
        """
        birth_year = get_year_from_date(self.student.get_dob())
        if birth_year is None:
            logger.warning(
                "DOB not available for student PEN: %s",
                self.student.get_student_pen()
            )
        return birth_year

    def _get_birth_year_from_adhaar_dob(self):
        """
        Extract the birth year from the student's Aadhaar DOB.

        Returns:
            int | None: Birth year if Aadhaar DOB is valid, otherwise None.
        """
        birth_year = get_year_from_date(self.student.get_adhaar_dob())
        if birth_year is None:
            logger.warning(
                "Aadhaar DOB not available for student PEN: %s",
                self.student.get_student_pen()
            )
        return birth_year

    def _prepare_yob_trials(self):
        """
        Prepare a list of candidate Year of Birth (YOB) values for PEN search
        fallback.

        Strategy:
        1. Use student DOB and Aadhaar DOB if available.
        2. If both are missing, infer YOB from class using CLASS_AGE_MAP.
        3. Expand each base YOB with ±MAX_YOB_TRIAL_RANGE and deduplicate.

        Returns:
            List[int]: Candidate YOBs for fallback PEN search.
        """
        birth_year = self._get_birth_year_from_dob()
        aadhaar_birth_year = self._get_birth_year_from_adhaar_dob()
        yob_trial = [birth_year, aadhaar_birth_year]
        yob_trial = [yob for yob in yob_trial if yob is not None]

        # If DOB is missing, infer YOB from class
        if birth_year is None:
            logger.error(
                "Student DOB is missing for PEN: %s. "
                "Trying with class-age-based YOBs map.",
                self.student.get_student_pen()
            )
            class_level = self.student.get_class()
            age_for_class = CLASS_AGE_MAP.get(class_level)

            if age_for_class is not None:
                base_yob = CURRENT_YEAR - age_for_class
                for yob in range(base_yob - MAX_YOB_TRIAL_RANGE,
                                 base_yob + MAX_YOB_TRIAL_RANGE + 1):
                    yob = str(yob)
                    if yob not in yob_trial:
                        yob_trial.append(yob)
            else:
                logger.warning(
                    "Class level '%s' not found in CLASS_AGE_MAP for PEN: %s",
                    class_level,
                    self.student.get_student_pen()
                )

        logger.info(
            "YOB trials for student PEN %s: %s",
            self.student.get_student_pen(),
            yob_trial
        )

        return yob_trial
