"""
student_data.py

Provides a centralized data handler for parsed student records.

This module defines the `StudentData` class, which encapsulates student data
and exposes methods for retrieving and updating individual student entries.
It is designed to decouple data mutation logic from parsing workflows,
supporting modular design and traceable updates.

Includes:
    - Timestamped updates to student records
    - Logging for mutation and error tracking
    - Dictionary-based data access for downstream workflows

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-10-03
Last Modified: 2025-10-03

Version: 1.0.0
"""

from common.logger import logger
from utils.date_time_utils import get_timestamp


class StudentData:
    """
    Encapsulates parsed student data and provides update utilities.

    This class holds a dictionary of student records, keyed by a unique
    identifier (typically PEN number or Aadhaar suffix),
    and allows controlled updates to individual entries.
    It supports timestamped mutation and logging for traceability.

    Attributes:
        student_data (dict): Dictionary of student records keyed by unique ID.
    """

    def __init__(self, student_data):
        """
        Initializes the StudentData instance with parsed student records.

        Args:
            student_data (dict): Dictionary containing student records,
                keyed by a unique identifier
                (e.g., PEN number or Aadhaar suffix).
        """
        self.student_data = student_data

    def update_student_data(self, main_key, kwargs):
        """
        Updates the student record identified by `main_key` with new
        key-value pairs.

        If the student exists in the internal dictionary, the method applies
        the updates and appends a timestamp under the "Date and Time" field.
        If the student is not found, a warning is logged.

        Args:
            main_key (str): Unique identifier for the student
                            (e.g., PEN number).
            kwargs (dict): Dictionary of fields to update for the student.

        Returns:
            None

        Side Effects:
            - Mutates the internal `student_data` dictionary.
            - Adds a timestamp to the updated record.
            - Logs debug or warning messages for traceability.
        """

        if main_key in self.student_data:
            for key, value in kwargs.items():
                self.student_data[main_key][key] = value
                logger.debug("Updated %s: %s - %s", main_key, key, value)
            self.student_data[main_key]["Date and Time"] = get_timestamp(
                format="%d-%m-%Y - %I:%M:%S %p")
        else:
            logger.warning("%s not found in student data. No update made.",
                           main_key)

    def get_student_data(self):
        """
        Retrieves the full student data dictionary.

        Returns:
            dict: All student records keyed by their unique identifiers.
        """
        return self.student_data
