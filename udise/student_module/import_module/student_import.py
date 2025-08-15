"""
Automates UDISE Import Module using Selenium.
Includes functions to interact with Student Import Module
and handle exceptions.
"""

# from logger_setup import logger

import time

from selenium.webdriver.common.by import By

from autoedu.common import wait_and_click
from udise.student_module.ui import StudentImportUI


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
        wait_and_click((By.XPATH, StudentImportUI.STUDENT_MOVEMENT_PROGRESSION_XPATH))
        time.sleep(5)

        # Select  ProgreImport Activity from the list
        wait_and_click((By.XPATH, StudentImportUI.IMPORT_OPTION_XPATH))
        time.sleep(5)

    def import_student(self):
        pass
