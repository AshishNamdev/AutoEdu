import time

from selenium.common.exceptions import TimeoutException

from common.driver import driver
from common.logger import logger
from ui.udise.login import AcademicChoice, SchoolInformation, StudentLogin
from utils.utils import wait_and_click, wait_and_find_element


def student_module_login(username, password, max_attempts=3):
    """
    Attempts to log in to the UDISE student module with retries for invalid CAPTCHA or incorrect credentials.

    Parameters:
        username (str): The username to authenticate with.
        password (str): The password associated with the username.
        max_attempts (int): Maximum number of login attempts before giving up.

    Raises:
        Exception: If login fails after max_attempts.
    """
    logger.info("Starting login to UDISE Student Module")

    for attempt in range(1, max_attempts + 1):
        logger.info(f"Login attempt {attempt}/{max_attempts}")

        # Fill credentials
        elem = wait_and_find_element(StudentLogin.USERNAME)
        elem.clear()
        elem.send_keys(username)

        elem = wait_and_find_element(StudentLogin.PASSWORD)
        elem.clear()
        elem.send_keys(password)

        wait_and_click(StudentLogin.CAPTCHA)

        logger.info("Waiting 15 seconds for manual CAPTCHA entry")
        time.sleep(15)

        wait_and_click(StudentLogin.SUBMIT_BUTTON)
        logger.info("Clicked on the Submit button to initiate login")

        # Give UI a moment to render any error messages
        time.sleep(2)

        if invalid_captcha():
            logger.warning("Invalid CAPTCHA detected. Retrying login...")
            continue

        if incorrect_creds():
            logger.warning("Incorrect credentials detected. Retrying login...")
            continue

        # If no errors, assume login success
        logger.info("Login successful. Proceeding to academic year selection.")
        time.sleep(2)
        select_academic_year()
        return

    # If loop completes without successful login
    raise Exception("Login failed after maximum attempts due to repeated CAPTCHA or credential errors.")


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
    logger.info("Selected Current Academic Year")

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
    logger.info("Closed School Information dialog popup")
    time.sleep(1)


def invalid_captcha():
    """
    Checks whether the CAPTCHA validation message indicates an invalid input.

    This function waits for the CAPTCHA message element to appear on the student login page,
    retrieves its inner HTML content, and returns True if the message contains the word "Invalid".

    Returns:
        bool: True if the CAPTCHA message contains "Invalid", False otherwise.
    """
    time.sleep(2)  # Give UI a moment to render error messages
    elements = driver.find_elements(*StudentLogin.ERROR_ALERT)
    if elements:
        msg = elements[0].get_attribute("innerHTML")
        logger.info(f"CAPTCHA error message: {msg}")
        return "Invalid" in msg if msg else False
    return False


def incorrect_creds():
    """
    Checks if the login failure was due to incorrect username or password.

    This function retrieves the inner HTML of the element associated with invalid login messages.
    It logs the message content and returns True if the message contains the keyword 'Incorrect',
    indicating a credential-related failure.

    Returns:
        bool: True if the message indicates incorrect credentials, False otherwise.
    """
    time.sleep(2)  # Give UI a moment to render error messages
    elements = driver.find_elements(*StudentLogin.ERROR_ALERT)
    if elements:
        msg = elements[0].get_attribute("innerHTML")
        logger.info(f"Credential error message: {msg}")
        return "Incorrect" in msg if msg else False
    return False
