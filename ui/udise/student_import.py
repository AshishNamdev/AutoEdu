from selenium.webdriver.common.by import By


class StudentImportUI:

    # Selectors

    # XPath selectors
    # MOVEMENT_PROGRESSION_XPATH = '//*[@id="collapseList"]/span'
    MOVEMENT_PROGRESSION_XPATH = "//div/ul/li[8]/div/div/h2/button/span"
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

    # Locators
    STUDENT_MOVEMENT_PROGRESSION = (By.XPATH, MOVEMENT_PROGRESSION_XPATH)
    STUDENT_IMPORT_OPTION = (By.XPATH, IMPORT_OPTION_XPATH)
