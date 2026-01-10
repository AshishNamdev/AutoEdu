"""
Module: ui.selectors.udise

This module defines a collection of UI selectors used in the
UDISE Student Section Shift interface.
Selectors are organized by strategy type
(XPath, ID, CSS, Name, Class Name) and are used to
locate and interact with specific elements on the web page during
automated testing or UI operations.

These selectors serve as constants for building reliable and maintainable
automation scripts.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2026-01-10

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
    STUDENT_NAME_XPATH = (
        "//li[span[1][contains(text(), 'Student Name')]]/span[2]"
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


class SearchPENSelectors:
    """
    XPath selectors for locating elements on the 'Search PEN' UI page.

    This class provides centralized, resilient XPath strings for all key UI
    components involved in the Search PEN workflow. These selectors are
    consumed by locator classes (e.g., SearchPENLocators) and used in
    automation scripts to interact with the page.

    Usage:
        driver.find_element(
            By.XPATH,
            SearchPENSelectors.AADHAAR_NO_XPATH
        ).send_keys("123456789012")
        driver.find_element(
            By.XPATH,
            SearchPENSelectors.SEARCH_BUTTON_XPATH
        ).click()

    Includes:
        - Input fields for Aadhaar and Year of Birth
        - Action buttons for search and data retrieval
        - Display fields for PEN and DOB
        - Status messaging and modal controls

    Attributes:
        GET_PEN_AND_DOB_BUTTON_XPATH (str):
            XPath for the 'Get PEN' link or button.
            Anchored by visible text using normalize-space for whitespace
            tolerance.
        AADHAAR_NO_XPATH (str):
            XPath for the Aadhaar number input field.
            Targets input by name attribute for schema resilience.
        YEAR_OF_BIRTH_XPATH (str):
            XPath for the date of birth input field.
            Uses name='dob' for consistent schema targeting.
        SEARCH_BUTTON_XPATH (str):
            XPath for the 'Search' button.
            Anchored by visible text with whitespace normalization.
        STATUS_MESSAGE_XPATH (str):
            XPath for the status message dialog header.
            Targets modal header using ARIA role for accessibility resilience.
        STUDENT_PEN_XPATH (str):
            XPath for the first student's PEN value in the results table.
            Dynamically anchored to the 'Student PEN' header for column-index
            independence.
        STUDENT_DOB_XPATH (str):
            XPath for the first student's date of birth in the results table.
            Anchored to the 'DOB' header for resilient column targeting.
        CLOSE_BUTTON_XPATH (str):
            XPath for the 'Close' button in dialogs.
            Uses ARIA label for accessibility and styling independence.
    """
    GET_PEN_AND_DOB_BUTTON_XPATH = (
        "//a[contains(normalize-space(text()), 'Get PEN')]"
    )
    AADHAAR_NO_XPATH = "//input[@name='aadhaar']"
    YEAR_OF_BIRTH_XPATH = "//input[@name='dob']"
    SEARCH_BUTTON_XPATH = (
        "//button[contains(normalize-space(text()), 'Search')]"
    )
    ERROR_MESSAGE_XPATH = "//div[@role='dialog']/h2"
    STUDENT_PEN_XPATH = (
        "//table//thead//th[normalize-space()='Student PEN']"
        "/ancestor::table//tbody/tr[1]/td[1]"
    )
    STUDENT_DOB_XPATH = (
        "//table//thead//th[normalize-space()='DOB']"
        "/ancestor::table//tbody/tr[1]/td[2]"
    )
    CLOSE_BUTTON_XPATH = "//button[@aria-label='Close']"
    ERROR_OK_BUTTON_XPATH = (
        "//button[contains(normalize-space(text()),'Okay')]"
    )


class StudentSectionShiftSelectors:
    """
    Centralized selector definitions for the UDISE Student Section Shift page.

    This class provides a structured collection of XPath and tag-based
    selectors used to locate UI elements on the Student Section Shift
    interface. These constants are consumed by automation scripts and Page
    Object classes to interact with dropdowns, buttons, tables, confirmation
    dialogs, and status messages in a consistent and maintainable way.

    Attributes
    ----------
    SECTION_SHIFT_OPTION_XPATH : str
        XPath for the 'Section Shift' menu option.
    SELECT_CLASS_DROPDOWN_XPATH : str
        XPath for the Class selection dropdown.
    SELECT_SECTION_DROPDOWN_XPATH : str
        XPath for the Section selection dropdown.
    GO_BUTTON_XPATH : str
        XPath for the 'Section Shift' Go button.
    NEXT_PAGE_BUTTON_XPATH : str
        XPath for the paginator Next button.
    STUDENT_COUNT_XPATH : str
        XPath for the element displaying total student count.
    SECTION_SHIFT_TABLE_XPATH : tuple[str, str]
        XPaths for locating the Section Shift data table container.
    TABLE_ROW_XPATH : str
        XPath for all table rows within the Section Shift table.
    NEW_SECTION_XPATH : str
        Relative XPath for the new Section dropdown inside each row.
    UPDATE_BUTTON_XPATH : str
        Relative XPath for the Update button inside each row.
    OK_BUTTON_XPATH : str
        XPath for the confirmation dialog OK button.
    STATUS_MESSAGE_XPATH : str
        XPath for the success message displayed after updating a section.
    STUDENT_PEN_UI_ROW_XPATH : str
        Relative XPath for the Student PEN cell within a table row.
    STUDENT_SECTION_UI_ROW_XPATH : str
        Relative XPath for the Student Section cell within a table row.
    TABLE_COLUMN_TAG : str
        Tag name used to identify table column elements.
    """

    SECTION_SHIFT_OPTION_XPATH = (
        "//span[contains(normalize-space(text()), 'Section Shift')]")
    SELECT_CLASS_DROPDOWN_XPATH = (
        "//label[contains(normalize-space(text()), 'Class')]"
        "/parent::li/following-sibling::li/select"
    )
    SELECT_SECTION_DROPDOWN_XPATH = (
        "//label[contains(normalize-space(text()), 'Section')]"
        "/parent::li/following-sibling::li/select"
    )
    GO_BUTTON_XPATH = (
        "//button[contains(normalize-space(text()), 'Go')]"
    )
    NEXT_PAGE_BUTTON_XPATH = "//mat-paginator//button[2]//span[3]"
    STUDENT_COUNT_XPATH = (
        "//div[contains(@class,'mat-mdc-paginator-range-label')]"
    )
    SECTION_SHIFT_TABLE_XPATH = "//table[@role='table' and contains(@class,'mat-mdc-table')]"
    TABLE_ROW_XPATH = "//tbody/tr"
    NEW_SECTION_XPATH = "./td[5]/select"
    UPDATE_BUTTON_XPATH = "./td[6]/button[normalize-space()='Update']"
    OK_BUTTON_XPATH = "//button[contains(normalize-space(text()), 'Okay')]"
    '''
    STATUS_MESSAGE_XPATH = (
        "//h2[contains(@class, 'swal2-title') and "
        "contains(normalize-space(text()), "
        "'Section Successfully Updated')]"
    )
    '''
    STATUS_MESSAGE_XPATH = "//html/body/div[4]/div/h2"
    STUDENT_PEN_UI_ROW_XPATH = "./td[2]"
    STUDENT_SECTION_UI_ROW_XPATH = "./td[1]/ul/li[2]/span"

    # Tag selectors
    TABLE_COLUMN_TAG = "td"
