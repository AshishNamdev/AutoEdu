import time

from autoedu.common import launch_browser, wait_and_click, wait_and_find_element
from udise.student_module.config import PASSWORD, URL, USERNAME
from udise.student_module.locators import (
    AcademicChoiceLocators,
    LoginLocators,
    SchoolInformationLocators,
)


def login_user():
    """
    Login User to System
    """
    launch_browser(URL)

    wait_and_find_element(LoginLocators.USERNAME).send_keys(USERNAME)

    wait_and_find_element(LoginLocators.PASSWORD).send_keys(PASSWORD)

    wait_and_click(LoginLocators.CAPTCHA)

    # Wait for 15 seconds for captcha mannual entry
    time.sleep(15)

    wait_and_click(LoginLocators.SUBMIT_BUTTON)
    time.sleep(10)
    select_academic_year()


def select_academic_year():
    """
    Click on current Acedamic Year
    """
    wait_and_click(AcademicChoiceLocators.ACADEMIC_YEAR)
    close_school_info()


def close_school_info():
    """
    Close the School Information pop up.
    """
    wait_and_click(SchoolInformationLocators.SCHOOL_INFO)
    time.sleep(1)
