"""
student.py

Defines the Student class for accessing structured student metadata from
imported datasets. This class provides convenient accessors for commonly
used student attributes such as class, section, name, and Aadhaar details.

Intended for use in educational automation workflows where student records
are parsed and processed from centralized import files.

Classes:
    - Student: Encapsulates student data and exposes attribute-level access.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-08-21
Last Modified: 2025-08-23

Version: 1.0.1
"""

from common.utils import convert_to_ddmmyyyy


class Student:
    """
    Represents a student record parsed from import data.

    This class provides attribute-level access to student metadata using
    accessor methods. It is designed to work with a dictionary of student
    records keyed by PEN (Permanent Enrollment Number).

    Attributes:
        student_pen (str): Unique identifier for the student.
        import_data (dict): Dictionary containing all student records.
    """

    def __init__(self, student_pen, student_import_data):
        """
        Initializes a Student instance with a PEN and import data.

        Args:
            student_pen (str): Unique identifier for the student.
            student_import_data (dict): Dictionary of all student records.
        """

        self.import_data = student_import_data
        self.student_pen = student_pen

    def get_class(self):
        """
        Returns the academic class of the student.

        Returns:
            str: Class level (e.g., "9", "12").
        """

        return self.import_data["class"]

    def get_section(self):
        """
        Returns the section assigned to the student.

        Returns:
            str: Section name (e.g., "A", "C").
        """

        return self.import_data["section"]

    def get_admission_date(self):
        """
        Returns the date of admission of the student.

        Returns:
            str: Date of birth in DD/MM/YYYY format.
        """

        return convert_to_ddmmyyyy(self.import_data["admission_date"])

    def get_name(self):
        """
        Returns the full name of the student.

        Returns:
            str: Student's name.
        """

        return self.import_data["student_name"]

    def get_father_name(self):
        """
        Returns the name of the student's father.

        Returns:
            str: Father's name.
        """

        return self.import_data["father_name"]

    def get_mother_name(self):
        """
        Returns the name of the student's mother.

        Returns:
            str: Mother's name.
        """

        return self.import_data["mother_name"]

    def get_dob(self):
        """
        Returns the date of birth of the student.

        Returns:
            str: Date of birth in DD/MM/YYYY format.
        """

        return convert_to_ddmmyyyy(self.import_data["dob"])

    def get_adhaar_name(self):
        """
        Returns the Aadhaar name associated with the student.

        Returns:
            str: Aadhaar name (may be empty if not available).
        """

        return self.import_data["adhaar_name"]

    def get_adhaar_dob(self):
        """
        Returns the Aadhaar date of birth associated with the student.

        Returns:
            str: Aadhaar DOB (may be empty if not available).
        """

        return convert_to_ddmmyyyy(self.import_data["adhaar_dob"])

    def get_adhaar_last_digits(self):
        """
        Returns the last four digits of the student's Aadhaar number.

        Returns:
            str: Last four digits of Aadhaar.
        """

        return self.import_data["addhar_last_4_digits"]
