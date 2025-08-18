import time

from common import wait_and_click, wait_and_find_element
from udise.student_module.locators import (
    AcademicChoiceLocators,
    LoginLocators,
    SchoolInformationLocators,
)


def teacher_module_login(username, password):
    """
    Logs in to the UDISE teacher module using provided credentials.

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

    wait_and_find_element(LoginLocators.USERNAME).send_keys(username)

    wait_and_find_element(LoginLocators.PASSWORD).send_keys(password)

    wait_and_click(LoginLocators.CAPTCHA)

    # Wait for 15 seconds for captcha mannual entry
    time.sleep(15)

    wait_and_click(LoginLocators.SUBMIT_BUTTON)
    time.sleep(10)
