"""
Module: student_import_selector

Description:

This module defines a collection of UI selectors used in the
UDISE Student Import interface.
Selectors are organized by strategy type
(XPath, ID, CSS, Name, Class Name) and are used to
locate and interact with specific elements on the web page during
automated testing or UI operations.

These selectors serve as constants for building reliable and maintainable
automation scripts.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-09-23

Version: 1.0.0
"""


class StudentLoginSelectors:
    """
    A centralized collection of UI selectors for the UDISE Student Login
    interface.

    This class defines constants for locating key elements on the login page
    using various selector strategies. These selectors are used in automation
    scripts to interact with the login form, CAPTCHA field, error messages,
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
    CURRENT_SCHOOL_XPATH = (
        "//label[contains(normalize-space(text()), 'School Name')]"
        "/following::span[1]"
    )

    # Class name selectors
    USERNAME_CLASS = "form-control"

    # ID selectors
    PASSWORD_ID = "password-field"
    SUBMIT_BUTTON_ID = "submit-btn"
    CAPTCHA_ID = "captcha"


class StudentImportSelectors:
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
    MOVEMENT_PROGRESSION_XPATH = (
        "//span[contains(normalize-space(text()), "
        "'Student Movement and Progression')]"
        "/ancestor::button"
    )
    IMPORT_OPTION_XPATH = (
        '//*[@id="flush-collapseOne2"]/div/ul/li[2]/span'
    )
    STATUS_MESSAGE_XPATH = (
        "//div[@class='status-message']"
    )
    IN_STATE_IMPORT_XPATH = (
        "//ul/li[1]/div/button"
    )
    OUT_STATE_IMPORT_XPATH = (
        "//ul/li[2]/div/button"
    )
    IMPORT_GO_BUTTON_XPATH = (
        "//div[@class='col-lg-8']/ul/li[3]/button"
    )
    DOB_MISMATCH_MESSAGE_XPATH = (
        "//div[@role='dialog']/h2"
    )
    DOB_MISMATCH_OK_BUTTON_XPATH = (
        "//div[@class='swal2-actions']/button[1]"
    )
    CURRENT_SCHOOL_XPATH = (
        "//span[contains(normalize-space(text()), "
        "'School Name')]/following-sibling::span"
    )

    # XPath that matches either greenBack or redBack status container
    STUDENT_STATUS_XPATH = (
        "//*[contains(@class, 'greenBack') or "
        "contains(@class, 'redBack')]"
    )
    SELECT_CLASS_XPATH = (
        "//ul[@class='existingSchool1']/li[1]/div/select"
    )
    SELECT_SECTION_XPATH = (
        "//ul[@class='existingSchool1']/li[2]/div/ul/"
        "li[1]/select"
    )
    DOA_XPATH = (
        "//label[contains(text(), 'Date of Admission')]"
        "/following::input[contains(@placeholder, 'DD/MM')][1]"
    )
    IMPORT_BUTTON_XPATH = (
        "//ul[@class='existingSchool1']/li[4]/button"
    )
    IMPORT_CONFIRM_BUTTON_XPATH = (
        "//div[@class='swal2-actions']/button[3]"
    )
    IMPORT_OK_BUTTON_XPATH = (
        "//div[@class='swal2-actions']/button[1]"
    )
    IMPORT_SUCCES_MESSAGE_XPATH = (
        "//h2[contains(@class, 'swal2-title') and "
        "contains(normalize-space(text()), "
        "'Student successfully Imported')]"
    )

    # ID selectors
    STUDENT_PEN_ID = "mat-input-0"
    DOB_ID = "mat-input-1"
    DOA_ID = "mat-input-4"
    IMPORT_SUCCES_MESSAGE_ID = "swal2-title"


class ReleaseRequestSelectors:
    """
    A collection of XPath selectors used for automating interactions with the
    Release Request Management UI in the UDISE application.

    Attributes:
        RELEASE_REQUEST_MANAGEMENT_XPATH (str):
            XPath for the 'Release Request Management' menu item.
        IN_STATE_RELEASE_REQUEST_XPATH (str):
            XPath for the 'Within State' release request button.
        OUT_STATE_RELEASE_REQUEST_XPATH (str):
            XPath for the 'Outside State' release request button.
        GENERATE_RELEASE_REQUEST_XPATH (str):
            XPath for the 'Generate Student Release Request' button or link.
        STUDENT_PEN_XPATH (str):
            XPath for the input field to enter the student's PEN.
        DOB_XPATH (str):
            XPath for the 'Date of Birth' input field.
        GET_DETAILS_BUTTON_XPATH (str):
            XPath for the 'Get Details' button.
        SELECT_CLASS_XPATH (str):
            XPath for the class selection dropdown.
        SELECT_SECTION_XPATH (str):
            XPath for the section selection dropdown.
        DOA_XPATH (str):
            XPath for the 'Date of Admission' input field.
        SELECT_REMARK_XPATH (str):
            XPath for the remark selection dropdown.
        GENERATE_REQUEST_BUTTON_XPATH (str):
            XPath for the 'Generate' button to submit the release request.
        ERROR_MESSAGE_XPATH (str):
            XPath for the error message dialog indicating the student is
            currently in Dropbox.
        ERROR_OK_BUTTON_XPATH (str):
            XPath for the 'Okay' button in the error dialog.
    """
    # XPath selectors
    RELEASE_REQUEST_MANAGEMENT_XPATH = (
        "//span[contains(normalize-space(text()), "
        "'Release Request Management')]/ancestor::li"
    )
    IN_STATE_RELEASE_REQUEST_XPATH = (
        "//h5[contains(normalize-space(text()), 'Within State')]"
        "/following-sibling::div/button"
    )
    OUT_STATE_RELEASE_REQUEST_XPATH = (
        "//h5[contains(normalize-space(text()), 'Outside State')]"
        "/following-sibling::div/button"
    )
    GENERATE_RELEASE_REQUEST_XPATH = (
        "//*[contains(normalize-space(text()), "
        "'Generate Student Release Request')]"
    )
    STUDENT_PEN_XPATH = (
        "//input[@placeholder='Enter PEN']"
    )
    DOB_XPATH = (
        "//label[contains(normalize-space(.), 'Date of Birth')]"
        "/following-sibling::div//input[@placeholder='DD/MM/YYYY']"
    )
    GET_DETAILS_BUTTON_XPATH = (
        "//button[contains(normalize-space(text()), 'Get Details')]"
    )
    SELECT_CLASS_XPATH = (
        "//label[contains(normalize-space(text()), 'Class')]"
        "/following-sibling::select"
    )
    SELECT_SECTION_XPATH = (
        "//label[contains(normalize-space(text()), 'Section')]"
        "/following-sibling::select"
    )
    DOA_XPATH = (
        "//label[contains(text(), 'Date of Admission')]"
        "/following::input[contains(@placeholder, 'DD/MM')][1]"
    )
    SELECT_REMARK_XPATH = (
        "//label[contains(normalize-space(text()), 'Remark')]"
        "/following-sibling::select"
    )
    GENERATE_REQUEST_BUTTON_XPATH = (
        "//button[contains(normalize-space(text()), 'Generate')]"
    )
    REQUEST_STATUS_MESSAGE_XPATH = "//div[@role='dialog']/h2"
    OK_BUTTON_XPATH = (
        "//button[contains(normalize-space(text()), 'Okay')]"
    )
