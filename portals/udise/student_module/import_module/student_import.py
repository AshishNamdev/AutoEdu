"""
Automates UDISE Import Module using Selenium.
Includes functions to interact with Student Import Module
and handle exceptions.
"""

# from logger_setup import logger


from ui.udise.student_import import StudentImportUI
from ui.udise.login import StudentLogin
from common.config import USERNAME, PASSWORD

class StudentImport:
    
    def __init__(self):

        StudentLogin().student_login(USERNAME, PASSWORD, max_attempts=3)

        self.import_ui = StudentImportUI()

    def init_student_import(self):
        """
        Initialize the student import process.
        This could include setting up connections, reading config, etc.
        """
        self.import_ui.select_import_options()

    def import_student(self):
        pass
