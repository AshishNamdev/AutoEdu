
import time

from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from import_module.ui import AcademicChoice, Login, SchoolInformation

from .config import PASSWORD, TIMEOUT, URL, USERNAME

# Setup WebDriver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


def wait_and_click(web_driver, locator):
    """_summary_

    Args:
        web_driver (_type_): _description_
        locator (_type_): _description_
    """
    element = WebDriverWait(web_driver, TIMEOUT).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()


def wait_and_find_element(driver, locator):

    elem = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator))
    return elem


def wait_and_find_elements(driver, locator):

    elements = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located(locator)
    )
    return elements


def launch_browser():
    """
    open and Maximize Browser window
    """
    driver.get(URL)
    driver.maximize_window()


def login_user():
    """
    Login User to System
    """
    launch_browser()

    input_element = driver.find_element(By.CLASS_NAME, Login.USERNAME_CLASS)
    input_element.send_keys(USERNAME)

    input_element = driver.find_element(By.ID, Login.PASSWORD_ID)
    input_element.send_keys(PASSWORD)

    driver.find_element(By.ID, Login.CAPTCHA_ID).click()
    time.sleep(15)

    login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, Login.SUBMIT_BUTTON_ID))
    )
    login_button.click()

    time.sleep(15)


def select_academic_year():
    """
    Click on current Acedamic Year
    """
    wait_and_click(driver, (By.XPATH, AcademicChoice.AC_YEAR_XPATH))
    close_school_info()


def close_school_info():
    """
    Close the School Information pop up.
    """
    wait_and_click(driver, (By.XPATH, SchoolInformation.SCHOOL_INFO_XPATH))
    time.sleep(1)
