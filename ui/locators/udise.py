"""
Module: student_import_locator

Defines locator tuples for UI elements used in the UDISE Student Import module.
These locators are used to identify and interact with specific components on
the web interface, such as the Student Movement and Progression option and
the Import module.

Dependencies:
- selenium.webdriver.common.by.By: for specifying locator strategies
- ui.selectors.udise.StudentImportSelectors:
  contains XPath strings for UI elements

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-12-11

Version: 1.0.0
"""

from selenium.webdriver.common.by import By

from ui.selectors.udise import (
    ReleaseRequestSelectors,
    SearchPENSelectors,
    StudentImportSelectors,
    StudentLoginSelectors,
    StudentSectionShiftSelectors,
)


class StudentLoginLocators:
    """
    Locator definitions for elements in the UDISE Student Login interface.

    This class provides static tuples that map UI components to their
    corresponding selectors, enabling automated interaction with login fields,
    CAPTCHA input, error messages, and post-login navigation elements such as
    academic year selection and school information dialogs.

    Usage:
        - Use with Selenium's `find_element` or `find_elements` to interact
          with login-related UI components.
        - Integrate into page object models for maintainable test automation.
        - Pair with `StudentLoginSelectors` to separate semantic meaning from
        structural location.

    Includes:
        - Login form fields: Username, Password, CAPTCHA
        - Action buttons: Submit
        - Error handling: Alert messages
        - Post-login navigation: Academic year selection, school info dialogs

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

        CURRENT_SCHOOL : tuple
            Locator for displaying the current school name after login
            (by XPath).
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
    corresponding XPath or ID selectors, enabling automated interaction
    with the Student Import interface using Selenium.

    Usage:
    - Use with Selenium's `find_element` or `find_elements` to interact with
      specific UI components.
    - Pair with `StudentImportSelectors` to maintain separation of structure
      and semantics.
    - Integrate into page object models for maintainable test automation.

    Includes:
    - Navigation options: Student Movement and Import modules
    - Form inputs: PEN, DOB, DOA, Class, Section
    - Status and feedback: Current School, Student Status, Success Message
    - Action buttons: GO, Import, Confirm, OK
    - Dialog handling: DOB mismatch message and confirmation

    Attributes:
    -----------
    STUDENT_MOVEMENT_PROGRESSION : tuple
        Locator for the 'Student Movement and Progression' option (by XPath).

    STUDENT_IMPORT_OPTION : tuple
        Locator for the 'Student Import' module option (by XPath).

    IN_STATE_IMPORT : tuple
        Locator for the In-State Import option (by XPath).

    OUT_STATE_IMPORT : tuple
        Locator for the Out-State Import option (by XPath).

    STUDENT_PEN : tuple
        Locator for the Student PEN input field (by ID).

    DOB : tuple
        Locator for the Date of Birth input field (by ID).

    IMPORT_GO_BUTTON : tuple
        Locator for the Import GO button (by XPath).

    DOB_MISMATCH_MESSAGE : tuple
        Locator for the DOB mismatch warning message (by XPath).

    DOB_MISMATCH_OK_BUTTON : tuple
        Locator for the OK button in the DOB mismatch dialog (by XPath).

    CURRENT_SCHOOL : tuple
        Locator for the current school display field (by XPath).

    STUDENT_STATUS : tuple
        Locator for the student status field (by XPath).

    SELECT_CLASS : tuple
        Locator for the class selection dropdown (by XPath).

    SELECT_SECTION : tuple
        Locator for the section selection dropdown (by XPath).

    DOA : tuple
        Locator for the Date of Admission input field (by XPath).

    IMPORT_BUTTON : tuple
        Locator for the Import button (by XPath).

    IMPORT_CONFIRM_BUTTON : tuple
        Locator for the confirmation button in the import dialog (by XPath).

    IMPORT_OK_BUTTON : tuple
        Locator for the OK button after successful import (by XPath).

    IMPORT_SUCCES_MESSAGE : tuple
        Locator for the success message displayed after import (by XPath).
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
    """
    Locators for elements on the Release Request Management UI.

    This class maps semantic element names to their corresponding XPath
    selectors, enabling consistent and maintainable access to UI components
    involved in release request workflows. These locators are used by
    automation scripts to interact with form fields, buttons, dropdowns,
    and status messages.

    Usage:
        - Pair with Selenium's `By.XPATH` to locate elements on the page.
        - Centralize selector management for easier updates and schema hygiene.
        - Support both in-state and out-state release request flows.

    Includes:
        - Form inputs: Student PEN, DOB, DOA, Class, Section, Remark
        - Action buttons: Get Details, Generate Request
        - Status indicators: Request Status Message, OK dialog button

    Attributes:
    -----------
    RELEASE_REQUEST_MANAGEMENT : tuple
        Locator for the Release Request Management section (by XPath).

    IN_STATE_RELEASE_REQUEST : tuple
        Locator for the In-State Release Request option (by XPath).

    OUT_STATE_RELEASE_REQUEST : tuple
        Locator for the Out-State Release Request option (by XPath).

    GENERATE_RELEASE_REQUEST : tuple
        Locator for the Generate Release Request button (by XPath).

    STUDENT_PEN : tuple
        Locator for the Student PEN input field (by XPath).

    DOB : tuple
        Locator for the Date of Birth input field (by XPath).

    GET_DETAILS_BUTTON : tuple
        Locator for the Get Details button (by XPath).

    SELECT_CLASS : tuple
        Locator for the Class selection dropdown (by XPath).

    SELECT_SECTION : tuple
        Locator for the Section selection dropdown (by XPath).

    DOA : tuple
        Locator for the Date of Admission input field (by XPath).

    SELECT_REMARK : tuple
        Locator for the Remark selection dropdown (by XPath).

    GENERATE_REQUEST_BUTTON : tuple
        Locator for the Generate Request button (by XPath).

    REQUEST_STATUS_MESSAGE : tuple
        Locator for the Request Status message (by XPath).

    OK_BUTTON : tuple
        Locator for the OK button in dialogs (by XPath).

    """

    RELEASE_REQUEST_MANAGEMENT = (
        By.XPATH,
        ReleaseRequestSelectors.RELEASE_REQUEST_MANAGEMENT_XPATH,
    )
    IN_STATE_RELEASE_REQUEST = (
        By.XPATH, ReleaseRequestSelectors.IN_STATE_RELEASE_REQUEST_XPATH)
    OUT_STATE_RELEASE_REQUEST = (
        By.XPATH, ReleaseRequestSelectors.OUT_STATE_RELEASE_REQUEST_XPATH)
    GENERATE_RELEASE_REQUEST = (
        By.XPATH, ReleaseRequestSelectors.GENERATE_RELEASE_REQUEST_XPATH)
    STUDENT_PEN = (By.XPATH, ReleaseRequestSelectors.STUDENT_PEN_XPATH)
    DOB = (By.XPATH, ReleaseRequestSelectors.DOB_XPATH)
    GET_DETAILS_BUTTON = (
        By.XPATH, ReleaseRequestSelectors.GET_DETAILS_BUTTON_XPATH)
    STUDENT_NAME = (
        By.XPATH, ReleaseRequestSelectors.STUDENT_NAME_XPATH)
    SELECT_CLASS = (By.XPATH, ReleaseRequestSelectors.SELECT_CLASS_XPATH)
    SELECT_SECTION = (
        By.XPATH, ReleaseRequestSelectors.SELECT_SECTION_XPATH)
    DOA = (By.XPATH, ReleaseRequestSelectors.DOA_XPATH)

    SELECT_REMARK = (By.XPATH, ReleaseRequestSelectors.SELECT_REMARK_XPATH)
    GENERATE_REQUEST_BUTTON = (
        By.XPATH, ReleaseRequestSelectors.GENERATE_REQUEST_BUTTON_XPATH)
    REQUEST_STATUS_MESSAGE = (
        By.XPATH, ReleaseRequestSelectors.REQUEST_STATUS_MESSAGE_XPATH)
    OK_BUTTON = (
        By.XPATH, ReleaseRequestSelectors.OK_BUTTON_XPATH)


class SearchPENLocators:
    """
    Locator definitions for the 'Search PEN' UI workflow.

    This class centralizes all XPath-based locators used in the Search PEN
    interface, enabling maintainable, scalable automation. Each locator is
    defined as a tuple compatible with Selenium's `find_element` and
    `find_elements` methods.

    Usage:
        driver.find_element(*SearchPENLocators.AADHAAR_NO).send_keys(
            "123456789012"
        )
        driver.find_element(
            *SearchPENLocators.SEARCH_BUTTON
        ).click()

    Includes:
        - Input fields for Aadhaar and Year of Birth
        - Action buttons for search and data retrieval
        - Display fields for PEN and DOB
        - Status messaging and modal controls

    Attributes:
        GETN_PEN_AND_DOB_BUTTON (tuple): Triggers retrieval of Student PEN
            and DOB.
        AADHAAR_NO (tuple): Input field for entering Aadhaar number.
        YEAR_OF_BIRTH (tuple): Input field for entering year of birth.
        SEARCH_BUTTON (tuple): Button to initiate search based on Aadhaar
            and DOB.
        STUDENT_PEN_VALUE (tuple): Field displaying the retrieved Student PEN.
        STUDENT_DOB_VALUE (tuple): Field displaying the retrieved Student DOB.
        STATUS_MESSAGE (tuple): Element showing success or error messages.
        CLOSE_BUTTON (tuple): Modal close button (typically top-right corner).
    """

    GET_PEN_AND_DOB_BUTTON = (
        By.XPATH,
        SearchPENSelectors.GET_PEN_AND_DOB_BUTTON_XPATH
    )
    AADHAAR_NO = (
        By.XPATH,
        SearchPENSelectors.AADHAAR_NO_XPATH
    )
    YEAR_OF_BIRTH = (
        By.XPATH,
        SearchPENSelectors.YEAR_OF_BIRTH_XPATH
    )
    SEARCH_BUTTON = (
        By.XPATH,
        SearchPENSelectors.SEARCH_BUTTON_XPATH
    )
    STUDENT_PEN_VALUE = (
        By.XPATH,
        SearchPENSelectors.STUDENT_PEN_XPATH
    )
    STUDENT_DOB_VALUE = (
        By.XPATH,
        SearchPENSelectors.STUDENT_DOB_XPATH
    )
    ERROR_MESSAGE = (
        By.XPATH,
        SearchPENSelectors.ERROR_MESSAGE_XPATH
    )
    CLOSE_BUTTON = (
        By.XPATH,
        SearchPENSelectors.CLOSE_BUTTON_XPATH
    )
    ERROR_OK_BUTTON = (
        By.XPATH,
        SearchPENSelectors.ERROR_OK_BUTTON_XPATH
    )


class StudentSectionShiftLocators:
    """
    Locators for the Student Section Shift page.

    This class defines all Selenium locator tuples used to interact with
    dropdowns, buttons, tables, and row-level actions on the Student Section
    Shift interface. Each locator references an XPath or tag selector defined
    in `StudentSectionShiftSelectors`, keeping the Page Object clean and
    maintainable.

    Attributes:
        SECTION_SHIFT_OPTION: Locator for the main Section Shift option.
        SELECT_CLASS_DROPDOWN: Locator for the Class selection dropdown.
        SELECT_SECTION_DROPDOWN: Locator for the Section selection dropdown.
        GO_BUTTON: Locator for the 'Go' button used to load table data.
        NEXT_PAGE: Locator for the pagination 'Next' button.
        SECTION_SHIFT_TABLE: Locator for the main table element.
        TABLE_ROW: Locator for table rows within the Section Shift table.
        NEW_SECTION: Locator for the dropdown used to select a new section.
        UPDATE_BUTTON: Locator for the Update button inside each table row.
        OK_BUTTON: Locator for the confirmation dialog OK button.
        STATUS_MESSAGE: Locator for the status or success message element.
        TABLE_COLUMN: Locator for table column elements (tag-based).
    """

    SECTION_SHIFT_OPTION = (
        By.XPATH, StudentSectionShiftSelectors.SECTION_SHIFT_OPTION_XPATH)
    SELECT_CLASS_DROPDOWN = (
        By.XPATH, StudentSectionShiftSelectors.SELECT_CLASS_DROPDOWN_XPATH)
    SELECT_SECTION_DROPDOWN = (
        By.XPATH, StudentSectionShiftSelectors.SELECT_SECTION_DROPDOWN_XPATH)
    GO_BUTTON = (By.XPATH, StudentSectionShiftSelectors.GO_BUTTON_XPATH)
    NEXT_PAGE = (By.XPATH, StudentSectionShiftSelectors.NEXT_PAGE_XPATH)
    SECTION_SHIFT_TABLE = (
        By.XPATH, StudentSectionShiftSelectors.SECTION_SHIFT_TABLE_XPATH)
    TABLE_ROW = (By.XPATH, StudentSectionShiftSelectors.TABLE_ROW_XPATH)
    NEW_SECTION = (By.XPATH, StudentSectionShiftSelectors.NEW_SECTION_XPATH)
    UPDATE_BUTTON = (
        By.XPATH, StudentSectionShiftSelectors.UPDATE_BUTTON_XPATH)
    OK_BUTTON = (By.XPATH, StudentSectionShiftSelectors.OK_BUTTON_XPATH)
    STATUS_MESSAGE = (
        By.XPATH, StudentSectionShiftSelectors.STATUS_MESSAGE_XPATH)
    TABLE_COLUMN = (By.TAG_NAME, StudentSectionShiftSelectors.TABLE_COLUMN_TAG)
