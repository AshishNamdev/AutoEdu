from selenium.webdriver.common.by import By


class StudentLogin:

    # Selectors
    # Xpath selectors

    # INVALID_CAPTCHA_XPATH = "//div/div[2]/div/div/div/div/div/span"
    ERROR_ALERT_XPATH = "//div[@role='alert']/div/span"

    # Class name selectors
    USERNAME_CLASS = "form-control"

    # ID selectors
    PASSWORD_ID = "password-field"
    SUBMIT_BUTTON_ID = "submit-btn"
    CAPTCHA_ID = "captcha"

    # Locators
    USERNAME = (By.CLASS_NAME, USERNAME_CLASS)
    PASSWORD = (By.ID, PASSWORD_ID)
    CAPTCHA = (By.ID, CAPTCHA_ID)
    SUBMIT_BUTTON = (By.ID, SUBMIT_BUTTON_ID)
    ERROR_ALERT = (By.XPATH, ERROR_ALERT_XPATH)


class AcademicChoice:

    # Selectors

    # XPath selectors
    AC_YEAR_XPATH = "//ul/li/div/div[2]/p"

    # Locators
    ACADEMIC_YEAR = (By.XPATH, AC_YEAR_XPATH)


class SchoolInformation:

    # Selectors
    # XPath selectors
    SCHOOL_INFO_XPATH = "//div/div/div/div[3]/button"

    # Locators
    SCHOOL_INFO = (By.XPATH, SCHOOL_INFO_XPATH)
