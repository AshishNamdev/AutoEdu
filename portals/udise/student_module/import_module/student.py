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
Last Modified: 2025-09-28

Version: 1.0.0
"""


from utils.aadhaar_utils import AadhaarValidator
from utils.date_time_utils import convert_to_ddmmyyyy


class Student:
    """
    Represents a student record parsed from import data.

    This class provides attribute-level access to student metadata using
    accessor methods. It is designed to work with a dictionary of student
    records keyed by PEN (Permanent Enrollment Number).

    Attributes:
        student_pen (str): Unique identifier for the student.
        student_data (dict): Dictionary containing all student records.
    """

    def __init__(self, student_pen, student_data):
        """
        Initializes a Student instance with a PEN and import data.

        Args:
            student_pen (str): Unique identifier for the student.
            student_student_data (dict): Dictionary of all student records.
        """

        self.student_data = student_data
        self._student_pen = student_pen
        self._pen_dob = None
        self.current_school = None
        self.searched_pen_no = None

    def set_searched_pen_no(self, pen_no):
        """
        Sets the PEN number that was searched for this student.

        Args:
            pen_no (str): The PEN number found in search operations.
        """
        self.searched_pen_no = pen_no

    def get_searched_pen_no(self):
        """
        Retrieves the PEN number that was searched for this student.

        Returns:
            str: The PEN number found in search operations.
        """
        return self.searched_pen_no

    def get_student_pen(self):
        """
        Retrieves the student's Permanent Education Number (PEN).

        Returns:
            str: The PEN associated with the student.
        """
        return self._student_pen

    def set_pen_dob(self, dob):
        """
        Sets the Date of Birth (DOB) used for PEN validation.

        Args:
            dob (str): The date of birth to associate with the student's PEN
                record. Format should be 'YYYY-MM-DD' or as required by schema.
        """
        self._pen_dob = dob

    def set_current_school(self, school_name):
        """
        Sets the current school name for the student.

        Args:
            school_name (str): The name of the school where the student is
                currently enrolled.
        """
        self.student_data["current_school"] = school_name

    def get_current_school(self):
        """
        Retrieves the current school name for the student.

        Returns:
            str: The name of the school where the student is currently
                enrolled.
        """
        return self.student_data.get("current_school")

    def get_pen_dob(self):
        """
        Retrieves the Date of Birth (DOB) associated with the student's
        PEN record.

        Returns:
            str: The PEN DOB value, if set.
        """
        return self._pen_dob

    def get_class(self):
        """
        Returns the academic class of the student.

        Returns:
            str: Class level (e.g., "9", "12").
        """
        return self.student_data["class"]

    def get_section(self):
        """
        Returns the section assigned to the student.

        Returns:
            str: Section name (e.g., "A", "C").
        """
        return self.student_data["section"]

    def get_admission_date(self):
        """
        Retrieves the student's date of admission in DD/MM/YYYY format.

        This method accesses the 'admission_date' field from the imported data.
        If the field is empty, it returns None. Otherwise, it converts the date
        to DD/MM/YYYY format using the `convert_to_ddmmyyyy` utility.

        Returns:
            Optional[str]: The formatted admission date,
                            or None if not available.
        """
        doa = self.student_data["admission_date"]
        return (
            None
            if doa == "" or doa.lower() == "na"
            else convert_to_ddmmyyyy(doa)
        )

    def get_name(self):
        """
        Returns the full name of the student.

        Returns:
            str: Student's name.
        """
        return self.student_data["student_name"]

    def get_father_name(self):
        """
        Returns the name of the student's father.

        Returns:
            str: Father's name.
        """
        return self.student_data["father_name"]

    def get_mother_name(self):
        """
        Returns the name of the student's mother.

        Returns:
            str: Mother's name.
        """
        return self.student_data["mother_name"]

    def get_dob(self):
        """
        Returns the date of birth of the student.

        Returns:
            str: Date of birth in DD/MM/YYYY format.
        """
        dob = self.student_data["dob"]
        return None if dob == "" or "na" in dob else convert_to_ddmmyyyy(dob)

    def get_adhaar_name(self):
        """
        Returns the Aadhaar name associated with the student.

        Returns:
            str: Aadhaar name (may be empty if not available).
        """
        return self.student_data["adhaar_name"]

    def get_adhaar_dob(self):
        """
        Retrieves the student's Aadhaar-linked date of birth in DD/MM/YYYY
        format.

        This method checks the 'adhaar_dob' field from the imported data.
        If the field is empty, it returns None. Otherwise, it converts the date
        to DD/MM/YYYY format using the `convert_to_ddmmyyyy` utility.

        Returns:
            Optional[str]: The formatted Aadhaar date of birth,
                            or None if not available.
        """
        adhaar_dob = self.student_data["adhaar_dob"]
        return (
            None
            if adhaar_dob == "" or "na" in adhaar_dob
            else convert_to_ddmmyyyy(adhaar_dob)
        )

    def get_adhaar_number(self):
        """
        Returns the student's Aadhaar number.

        Returns:
            str: Last four digits of Aadhaar.
        """
        adhaar_no = self.student_data["adhaar_no."]
        return adhaar_no if AadhaarValidator.is_valid(adhaar_no) else None

    def get_adhaar_last_digits(self):
        """
        Returns the last four digits of the student's Aadhaar number.

        Returns:
            str: Last four digits of Aadhaar.
        """
        adhaar_no = self.get_adhaar_number()
        if isinstance(adhaar_no, str):
            return adhaar_no[-4:]
        return None
