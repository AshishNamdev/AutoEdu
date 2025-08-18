import time

from common import wait_and_click, wait_and_find_element
from ui import AcademicChoice, SchoolInformation, StudentLogin


def student_module_login(username, password):
    """
    Logs in to the UDISE student module using provided credentials.

    This function automates the login process by entering the given username
    and password into the appropriate fields on the UDISE portal. It assumes
    that the browser has already been launched and navigated to the login page.

    Parameters:
        username (str): The username to authenticate with.
        password (str): The password associated with the username.

    Returns:
        None

    Raises:
        Exception: If login fails due to missing elements or incorrect credentials.
    """

    wait_and_find_element(StudentLogin.USERNAME).send_keys(username)

    wait_and_find_element(StudentLogin.PASSWORD).send_keys(password)

    wait_and_click(StudentLogin.CAPTCHA)

    # Wait for 15 seconds for captcha mannual entry
    time.sleep(15)

    wait_and_click(StudentLogin.SUBMIT_BUTTON)
    time.sleep(10)
    select_academic_year()


def select_academic_year():
    """
    Selects the current academic year from the dropdown or list.

    This function locates and clicks on the academic year element using predefined
    locators. After selection, it closes any school information pop-up or modal
    that may appear as a result of the selection.

    Dependencies:
        - wait_and_click: Utility function to wait for and click UI elements.
        - AcademicChoiceLocators.ACADEMIC_YEAR: Locator for the academic year element.
        - close_school_info: Function to close school-related pop-ups.

    Returns:
        None
    """

    wait_and_click(AcademicChoice.ACADEMIC_YEAR)
    close_school_info()


def close_school_info():
    """
    Closes the school information pop-up window if it appears.

    This function detects and dismisses the school information modal or overlay
    that may block further interaction with the page. It ensures smooth workflow
    by removing UI interruptions after academic year selection or login.

    Dependencies:
        - wait_and_click or equivalent method to interact with the close button.
        - Locator for the school info close button (e.g., SchoolInfoLocators.CLOSE_BUTTON).

    Returns:
        None

    Raises:
        Exception: If the pop-up cannot be closed due to missing elements or UI issues.
    """

    wait_and_click(SchoolInformation.SCHOOL_INFO)
    time.sleep(1)
