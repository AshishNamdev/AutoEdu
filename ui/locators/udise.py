"""
Module: student_import_locator

Defines locator tuples for UI elements used in the UDISE Student Import module.
These locators are used to identify and interact with specific components on the
web interface, such as the Student Movement and Progression option and the Import module.

Dependencies:
- selenium.webdriver.common.by.By: for specifying locator strategies
- ui.selectors.udise.StudentImportSelector: contains XPath strings for UI elements

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-08-29

Version: 1.0.0
"""

from selenium.webdriver.common.by import By

from ui.selectors.udise import StudentImportSelector, StudentLoginSelector


class StudentLoginLocator:
    """
    Locator definitions for elements in the UDISE Student Login interface.

    This class provides static tuples that map UI components to their corresponding selectors,
    enabling automated interaction with login fields, CAPTCHA, error messages, and post-login
    navigation elements such as academic year selection and school information dialogs.

    Attributes:
    -----------
    USERNAME : tuple
        Locator for the username input field (by class name).

    PASSWORD : tuple
        Locator for the password input field (by ID).

    CAPTCHA : tuple
        Locator for the CAPTCHA input field (by ID).

    SUBMIT_BUTTON : tuple
        Locator for the login submit button (by ID).

    ERROR_ALERT : tuple
        Locator for error alert messages (by XPath).

    ACADEMIC_YEAR : tuple
        Locator for selecting the academic year after login (by XPath).

    SCHOOL_INFO : tuple
        Locator for closing the school information pop-up (by XPath).
    """

    USERNAME = (By.CLASS_NAME, StudentLoginSelector.USERNAME_CLASS)
    PASSWORD = (By.ID, StudentLoginSelector.PASSWORD_ID)
    CAPTCHA = (By.ID, StudentLoginSelector.CAPTCHA_ID)
    SUBMIT_BUTTON = (By.ID, StudentLoginSelector.SUBMIT_BUTTON_ID)
    ERROR_ALERT = (By.XPATH, StudentLoginSelector.ERROR_ALERT_XPATH)

    # Academic Choice Locators
    ACADEMIC_YEAR = (By.XPATH, StudentLoginSelector.AC_YEAR_XPATH)

    # School Information Locators
    SCHOOL_INFO = (By.XPATH, StudentLoginSelector.SCHOOL_INFO_XPATH)
    CURRENT_SCHOOL = (By.XPATH, StudentLoginSelector.CURRENT_SCHOOL_XPATH)


class StudentImportLocator:
    """
    Locator definitions for the UDISE Student Import UI module.

    This class provides static tuples that map UI elements to their
    corresponding XPath selectors, enabling automated interaction with
    the Student Import interface.

    Attributes:
    -----------
    STUDENT_MOVEMENT_PROGRESSION : tuple
        Locator for the 'Student Movement and Progression' option.

    STUDENT_IMPORT_OPTION : tuple
        Locator for the 'Student Import' module option.
    """

    STUDENT_MOVEMENT_PROGRESSION = (
        By.XPATH,
        StudentImportSelector.MOVEMENT_PROGRESSION_XPATH,
    )
    STUDENT_IMPORT_OPTION = (By.XPATH, StudentImportSelector.IMPORT_OPTION_XPATH)
    IN_STATE_IMPORT = (By.XPATH, StudentImportSelector.IN_STATE_IMPORT_XPATH)
    OUT_STATE_IMPORT = (By.XPATH, StudentImportSelector.OUT_STATE_IMPORT_XPATH)
    STUDENT_PEN = (By.ID, StudentImportSelector.STUDENT_PEN_ID)
    DOB = (By.ID, StudentImportSelector.DOB_ID)
    IMPORT_GO_BUTTON = (By.XPATH, StudentImportSelector.IMPORT_GO_BUTTON_XPATH)
    DOB_MISMATCH_MESSAGE = (By.XPATH, StudentImportSelector.DOB_MISMATCH_MESSAGE_XPATH)
    DOB_MISMATCH_OK_BUTTON = (
        By.XPATH,
        StudentImportSelector.DOB_MISMATCH_OK_BUTTON_XPATH,
    )
    CURRENT_SCHOOL = (By.XPATH, StudentImportSelector.CURRENT_SCHOOL_XPATH)
    STUDENT_STATUS = (By.XPATH, StudentImportSelector.STUDENT_STATUS_XPATH)
    SELECT_CLASS = (By.XPATH, StudentImportSelector.SELECT_CLASS_XPATH)
    SELECT_SECTION = (By.XPATH, StudentImportSelector.SELECT_SECTION_XPATH)
    DOA = (By.XPATH, StudentImportSelector.DOA_XPATH)
    IMPORT_BUTTON = (By.XPATH, StudentImportSelector.IMPORT_BUTTON_XPATH)
    IMPORT_CONFIRM_BUTTON = (
        By.XPATH,
        StudentImportSelector.IMPORT_CONFIRM_BUTTON_XPATH,
    )
    IMPORT_OK_BUTTON = (By.XPATH, StudentImportSelector.IMPORT_OK_BUTTON_XPATH)
    IMPORT_SUCCES_MESSAGE = (
        By.XPATH,
        StudentImportSelector.IMPORT_SUCCES_MESSAGE_XPATH
    )
