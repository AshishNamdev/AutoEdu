"""
Module: student_import_selector

Description:

This module defines a collection of UI selectors used in the UDISE Student Import interface.
Selectors are organized by strategy type (XPath, ID, CSS, Name, Class Name) and are used to
locate and interact with specific elements on the web page during automated testing or UI operations.

These selectors serve as constants for building reliable and maintainable automation scripts.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-19
Last Modified: 2025-08-19
Version: 1.0.0
"""

class StudentLoginSelector:
    """
    A centralized collection of UI selectors for the UDISE Student Login interface.

    This class defines constants for locating key elements on the login page using various selector strategies.
    These selectors are used in automation scripts to interact with the login form, CAPTCHA field, error messages,
    and academic year selection.

    Attributes:
    -----------
    XPath Selectors:
        AC_YEAR_XPATH : str
            XPath for selecting the academic year.
        SCHOOL_INFO_XPATH : str
            XPath for closing the school information pop-up.
        ERROR_ALERT_XPATH : str
            XPath for locating error alert messages.

    Class Name Selectors:
        USERNAME_CLASS : str
            Class name for the username input field.

    ID Selectors:
        PASSWORD_ID : str
            ID for the password input field.
        SUBMIT_BUTTON_ID : str
            ID for the login submit button.
        CAPTCHA_ID : str
            ID for the CAPTCHA input field.
    """

    # Xpath selectors

    AC_YEAR_XPATH = "//ul/li/div/div[2]/p" # Academic Choice
    SCHOOL_INFO_XPATH = "//div/div/div/div[3]/button" # School Information
    ERROR_ALERT_XPATH = "//div[@role='alert']/div/span"
    # INVALID_CAPTCHA_XPATH = "//div/div[2]/div/div/div/div/div/span"
    
    # Class name selectors
    USERNAME_CLASS = "form-control"

    # ID selectors
    PASSWORD_ID = "password-field"
    SUBMIT_BUTTON_ID = "submit-btn"
    CAPTCHA_ID = "captcha"

class StudentImportSelector:
    """
    A centralized repository of UI selectors for the UDISE Student Import module.

    Attributes:
    -----------
    XPath Selectors:
        MOVEMENT_PROGRESSION_XPATH : str
            XPath for the 'Student Movement and Progression' button.
        IMPORT_OPTION_XPATH : str
            XPath for the 'Student Import' option.
        FILE_UPLOAD_XPATH : str
            XPath for the file input element.
        SUBMIT_BUTTON_XPATH : str
            XPath for the import submission button.
        STATUS_MESSAGE_XPATH : str
            XPath for the status message display.

    ID Selectors:
        FILE_INPUT_ID : str
            ID for the student file input field.
        IMPORT_FORM_ID : str
            ID for the import form container.

    CSS Selectors:
        LOADING_SPINNER_CSS : str
            CSS selector for the loading spinner.
        ERROR_MESSAGE_CSS : str
            CSS selector for error messages.

    Name Selectors:
        FILE_FIELD_NAME : str
            Name attribute for the student file field.

    Class Name Selectors:
        SUCCESS_ALERT_CLASS : str
            Class name for success alert messages.
    """

    # XPath selectors
    # MOVEMENT_PROGRESSION_XPATH = '//*[@id="collapseList"]/span'
    MOVEMENT_PROGRESSION_XPATH = "//div/ul/li[9]/div/div/h2/button/span"
    IMPORT_OPTION_XPATH = '//*[@id="flush-collapseOne2"]/div/ul/li[2]/span'
    FILE_UPLOAD_XPATH = "//input[@type='file']"
    SUBMIT_BUTTON_XPATH = "//button[@id='submitImport']"
    STATUS_MESSAGE_XPATH = "//div[@class='status-message']"

    # ID selectors
    FILE_INPUT_ID = "studentFileInput"
    IMPORT_FORM_ID = "importForm"

    # CSS selectors
    LOADING_SPINNER_CSS = ".spinner.loading"
    ERROR_MESSAGE_CSS = ".error-message"

    # Name selectors
    FILE_FIELD_NAME = "student_file"

    # Class name selectors
    SUCCESS_ALERT_CLASS = "alert-success"