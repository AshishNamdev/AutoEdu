"""
Automates UDISE Import Module using Selenium.
Includes functions to interact with Student Import Module
and handle exceptions.
"""

# from logger_setup import logger

import time

from common import wait_and_click
from ui import StudentImportUI


class StudentImport:
    def __init__(self):
        self.student = None

    def init_student_import(self):
        """
        Initialize the student import process.
        This could include setting up connections, reading config, etc.
        """
        self.select_import_options()

    def select_import_options(self):
        """
        Select import options on UDISE Student Module.
        """
        # Select Student Movement and Progression option
        wait_and_click(StudentImportUI.STUDENT_MOVEMENT_PROGRESSION)
        time.sleep(5)

        # Select  ProgreImport Activity from the list
        wait_and_click(StudentImportUI.STUDENT_IMPORT_OPTION)
        time.sleep(5)

    def import_student(self):
        pass
