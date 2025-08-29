"""
Module: student_import_selector

Description:

This module defines a collection of UI selectors used in the UDISE Student Import interface.
Selectors are organized by strategy type (XPath, ID, CSS, Name, Class Name) and are used to
locate and interact with specific elements on the web page during automated testing or UI operations.

These selectors serve as constants for building reliable and maintainable automation scripts.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-08-29

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

    AC_YEAR_XPATH = "//ul/li/div/div[2]/p"  # Academic Choice
    SCHOOL_INFO_XPATH = "//div/div/div/div[3]/button"  # School Information
    ERROR_ALERT_XPATH = "//div[@role='alert']/div/span"
    CURRENT_SCHOOL_XPATH = "//label[contains(normalize-space(text()), 'School Name')]/following::span[1]"

    # Class name selectors
    USERNAME_CLASS = "form-control"

    # ID selectors
    PASSWORD_ID = "password-field"
    SUBMIT_BUTTON_ID = "submit-btn"
    CAPTCHA_ID = "captcha"


class StudentImportSelector:
    """
    A centralized repository of UI selectors for the
    UDISE Student Import module.

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
    MOVEMENT_PROGRESSION_XPATH = "//span[contains(normalize-space(text()), 'Student Movement and Progression')]/ancestor::button"
    IMPORT_OPTION_XPATH = '//*[@id="flush-collapseOne2"]/div/ul/li[2]/span'
    STATUS_MESSAGE_XPATH = "//div[@class='status-message']"
    IN_STATE_IMPORT_XPATH = "//ul/li[1]/div/button"
    OUT_STATE_IMPORT_XPATH = "//ul/li[2]/div/button"
    IMPORT_GO_BUTTON_XPATH = "//div[@class='col-lg-8']/ul/li[3]/button"
    DOB_MISMATCH_MESSAGE_XPATH = "//div[@role='dialog']/h2"
    DOB_MISMATCH_OK_BUTTON_XPATH = "//div[@class='swal2-actions']/button[1]"
    CURRENT_SCHOOL_XPATH = "//span[contains(normalize-space(text()), 'School Name')]/following-sibling::span"

    # XPath that matches either greenBack or redBack status container
    STUDENT_STATUS_XPATH = (
        "//*[contains(@class, 'greenBack') or contains(@class, 'redBack')]"
    )
    SELECT_CLASS_XPATH = "//ul[@class='existingSchool1']/li[1]/div/select"
    SELECT_SECTION_XPATH = "//ul[@class='existingSchool1']/li[2]/div/ul/li[1]/select"
    DOA_XPATH = "//label[contains(text(), 'Date of Admission')]/following::input[contains(@placeholder, 'DD/MM')][1]"
    IMPORT_BUTTON_XPATH = "//ul[@class='existingSchool1']/li[4]/button"
    IMPORT_CONFIRM_BUTTON_XPATH = "//div[@class='swal2-actions']/button[3]"
    IMPORT_OK_BUTTON_XPATH = "//div[@class='swal2-actions']/button[1]"
    IMPORT_SUCCES_MESSAGE_XPATH = "//h2[contains(@class, 'swal2-title') and contains(normalize-space(text()), 'Student successfully Imported')]"

    # ID selectors
    STUDENT_PEN_ID = "mat-input-0"
    DOB_ID = "mat-input-1"
    DOA_ID = "mat-input-4"
    IMPORT_SUCCES_MESSAGE_ID = "swal2-title"
