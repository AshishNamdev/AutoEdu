"""
Module: student_import_locator

Defines locator tuples for UI elements used in the UDISE Student Import module.
These locators are used to identify and interact with specific components on the
web interface, such as the Student Movement and Progression option and the Import module.

Dependencies:
- selenium.webdriver.common.by.By: for specifying locator strategies
- ui.selectors.udise.StudentImportSelectors: contains XPath strings for UI elements

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-09-23

Version: 1.0.0
"""

from selenium.webdriver.common.by import By

from ui.selectors.udise import StudentImportSelectors, StudentLoginSelectors


class StudentLoginLocators:
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

    USERNAME = (By.CLASS_NAME, StudentLoginSelectors.USERNAME_CLASS)
    PASSWORD = (By.ID, StudentLoginSelectors.PASSWORD_ID)
    CAPTCHA = (By.ID, StudentLoginSelectors.CAPTCHA_ID)
    SUBMIT_BUTTON = (By.ID, StudentLoginSelectors.SUBMIT_BUTTON_ID)
    ERROR_ALERT = (By.XPATH, StudentLoginSelectors.ERROR_ALERT_XPATH)

    # Academic Choice Locators
    ACADEMIC_YEAR = (By.XPATH, StudentLoginSelectors.AC_YEAR_XPATH)

    # School Information Locators
    SCHOOL_INFO = (By.XPATH, StudentLoginSelectors.SCHOOL_INFO_XPATH)
    CURRENT_SCHOOL = (By.XPATH, StudentLoginSelectors.CURRENT_SCHOOL_XPATH)


class StudentImportLocators:
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
        StudentImportSelectors.MOVEMENT_PROGRESSION_XPATH,
    )
    STUDENT_IMPORT_OPTION = (
        By.XPATH, StudentImportSelectors.IMPORT_OPTION_XPATH)
    IN_STATE_IMPORT = (By.XPATH, StudentImportSelectors.IN_STATE_IMPORT_XPATH)
    OUT_STATE_IMPORT = (
        By.XPATH, StudentImportSelectors.OUT_STATE_IMPORT_XPATH)
    STUDENT_PEN = (By.ID, StudentImportSelectors.STUDENT_PEN_ID)
    DOB = (By.ID, StudentImportSelectors.DOB_ID)
    IMPORT_GO_BUTTON = (
        By.XPATH, StudentImportSelectors.IMPORT_GO_BUTTON_XPATH)
    DOB_MISMATCH_MESSAGE = (
        By.XPATH, StudentImportSelectors.DOB_MISMATCH_MESSAGE_XPATH)
    DOB_MISMATCH_OK_BUTTON = (
        By.XPATH,
        StudentImportSelectors.DOB_MISMATCH_OK_BUTTON_XPATH,
    )
    CURRENT_SCHOOL = (By.XPATH, StudentImportSelectors.CURRENT_SCHOOL_XPATH)
    STUDENT_STATUS = (By.XPATH, StudentImportSelectors.STUDENT_STATUS_XPATH)
    SELECT_CLASS = (By.XPATH, StudentImportSelectors.SELECT_CLASS_XPATH)
    SELECT_SECTION = (By.XPATH, StudentImportSelectors.SELECT_SECTION_XPATH)
    DOA = (By.XPATH, StudentImportSelectors.DOA_XPATH)
    IMPORT_BUTTON = (By.XPATH, StudentImportSelectors.IMPORT_BUTTON_XPATH)
    IMPORT_CONFIRM_BUTTON = (
        By.XPATH,
        StudentImportSelectors.IMPORT_CONFIRM_BUTTON_XPATH,
    )
    IMPORT_OK_BUTTON = (
        By.XPATH, StudentImportSelectors.IMPORT_OK_BUTTON_XPATH)
    IMPORT_SUCCES_MESSAGE = (
        By.XPATH,
        StudentImportSelectors.IMPORT_SUCCES_MESSAGE_XPATH,
    )


class ReleaseRequestLocators:
    pass
