from selenium.webdriver.common.by import By
from .ui import Login, AcademicChoice, SchoolInformation


class LoginLocators:

    USERNAME = (By.CLASS_NAME, Login.USERNAME_CLASS)
    PASSWORD = (By.ID, Login.PASSWORD_ID)
    CAPTCHA = (By.ID, Login.CAPTCHA_ID)
    SUBMIT_BUTTON = (By.ID, Login.SUBMIT_BUTTON_ID)


class AcademicChoiceLocators:

    ACADEMIC_YEAR = (By.XPATH, AcademicChoice.AC_YEAR_XPATH)


class SchoolInformationLocators:

    SCHOOL_INFO = (By.XPATH, SchoolInformation.SCHOOL_INFO_XPATH)
