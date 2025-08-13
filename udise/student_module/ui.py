"""
Module for various UI selenium handlers
"""


class Login:
    """
    login Page UI Handlers
    """

    # Class name selectors
    USERNAME_CLASS = "form-control"

    # ID selectors
    PASSWORD_ID = "password-field"
    SUBMIT_BUTTON_ID = "submit-btn"
    CAPTCHA_ID = "captcha"


class AcademicChoice:
    """
    Academic Choice Page UI Handlers
    """

    # XPath selectors
    AC_YEAR_XPATH = "//ul/li/div/div[2]/p"


class SchoolInformation:
    """
    School Information Popup UI Handlers
    """

    # XPath selectors
    SCHOOL_INFO_XPATH = "//div/div/div/div[3]/button"


class StudentImportUI:
    """
    Student Import Module UI Handlers

    """

    # XPath selectors
    # STUDENT_MOVEMENT_PROGRESSION_XPATH = '//*[@id="collapseList"]/span'
    STUDENT_MOVEMENT_PROGRESSION_XPATH = "//div/ul/li[8]/div/div/h2/button/span"
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
