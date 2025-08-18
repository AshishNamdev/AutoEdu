"""
Utility functions for Selenium-based browser automation.

This module provides helper functions to wait for elements,
and perform robust clicking actions with retry logic.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-18
Last Modified: 2025-08-18
Version: 1.0.0

Functions:
    - wait_and_find_element(locator): Waits for a single clickable element.
    - wait_and_find_elements(locator): Waits for multiple elements to be present.
    - wait_and_click(locator, retries): Scrolls to and clicks an element with retry fallback.
"""

import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.config import TIMEOUT
from common.driver import driver


def wait_and_click(locator, retries=2):
    """
    Waits for an element to become clickable, scrolls to it, and attempts to click it.

    This function waits until the specified element is clickable, scrolls it into view
    using ActionChains, and performs a click. If the click is intercepted (e.g., by overlays),
    it retries using JavaScript-based clicking. Retries are configurable.

    Parameters:
        locator (tuple): A tuple specifying the strategy to locate the element,
                         e.g., (By.XPATH, "//button[@id='submit']").
        retries (int): Number of retry attempts if the standard click is intercepted.
                       Defaults to 2.

    Returns:
        None

    Raises:
        Exception: If the element cannot be clicked after the specified number of retries.
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
    """
    Waits for a web element to become clickable and returns it.

    This function uses WebDriverWait to poll the DOM until the specified
    element is clickable, within a predefined timeout period. It is useful
    for ensuring that dynamic elements are interactable before performing actions.

    Parameters:
        locator (tuple): A tuple specifying the strategy to locate the element,
                         e.g., (By.ID, "submit-button").

    Returns:
        WebElement: The Selenium WebElement once it becomes clickable.

    Raises:
        TimeoutException: If the element does not become clickable within the timeout.
    """
    elem = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator))
    return elem


def wait_and_find_elements(locator):
    """
    Waits for all elements matching the locator to be present in the DOM and returns them.

    This function uses WebDriverWait to wait until all elements specified by the locator
    are present in the DOM. It does not guarantee that the elements are visible or clickable,
    only that they exist in the page structure.

    Parameters:
        locator (tuple): A tuple specifying the strategy to locate the elements,
                         e.g., (By.CLASS_NAME, "item-row").

    Returns:
        list[WebElement]: A list of Selenium WebElements once they are located.

    Raises:
        TimeoutException: If the elements are not found within the timeout period.
    """
    elements = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located(locator)
    )
    return elements
