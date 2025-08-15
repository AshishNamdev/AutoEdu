import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from udise.student_module.config import TIMEOUT

# Setup WebDriver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


def wait_and_click(locator, retries=2):
    """
    Waits for an element to be clickable, scrolls to it, and clicks it.

    Args:
        locator (tuple): Selenium locator tuple (By.ID, "value")
        retries (int): Number of retry attempts if click is intercepted
    """
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable(locator)
            )

            # Scroll to element using ActionChains
            ActionChains(driver).scroll_to_element(element).perform()
            time.sleep(0.5)

            element.click()
            return  # Success

        except ElementClickInterceptedException:
            print(f"[Retry {attempt+1}] Click intercepted. Trying JS click fallback.")
            try:
                driver.execute_script("arguments[0].click();", element)
                return
            except Exception as js_error:
                print(f"JS click failed: {js_error}")
                time.sleep(1)

    raise Exception(f"Failed to click element after {retries} attempts: {locator}")


def wait_and_find_element(locator):

    elem = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator))
    return elem


def wait_and_find_elements(locator):

    elements = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located(locator)
    )
    return elements


def launch_browser(url):
    """
    open and Maximize Browser window
    """
    driver.get(url)
    driver.maximize_window()
