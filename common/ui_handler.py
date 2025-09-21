"""
ui_handler.py

Provides a reusable, resilient UIHandler class for interacting with web elements
using Selenium.

This module centralizes common UI automation patterns such as waiting for
elements, clicking, filling fields, scrolling, and verifying values. It is
designed to support modular, onboarding-friendly workflows with robust error
handling and traceable logging.

Key Features:
- Explicit waits for single and multiple elements
- Intelligent retries for flaky UI interactions
- Field filling and verification with scroll support
- Popup dismissal and element scrolling utilities
- Designed for schema-aware automation and CI/CD observability

Usage Example:
    from common.ui_handler import UIHandler as UI

    UI.fill_fields({
        (By.ID, "username"): "admin",
        (By.ID, "password"): "secret"
    })

Intended for use in AutoEdu workflows and other scalable automation platforms.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-09-21

Version: 1.0.0
"""

import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.config import TIMEOUT
from common.driver import WebDriverManager


class UIHandler:
    @classmethod
    def wait_and_click(cls, locator, retries=2):
        """
        Waits for an element to become clickable, scrolls to it, and
        attempts to click it.

        This function waits until the specified element is clickable,
        scrolls it into view using ActionChains, and performs a click.
        If the click is intercepted (e.g., by overlays), it retries
        using JavaScript-based clicking. Retries are configurable.

        Parameters:
            locator (tuple): A tuple specifying the strategy to locate
            the element, e.g., (By.XPATH, "//button[@id='submit']").
            retries (int): Number of retry attempts if the standard
            click is intercepted. Defaults to 2.

        Returns:
            None

        Raises:
            Exception: If the element cannot be clicked after the
            specified number of retries.
        """
        driver = WebDriverManager.get_driver()
        for attempt in range(retries):
            try:
                element = WebDriverWait(driver, TIMEOUT).until(
                    EC.element_to_be_clickable(locator)
                )

                # Scroll to element using ActionChains
                ActionChains(driver).scroll_to_element(element).perform()
                time.sleep(0.5)

                element.click()
                logger.debug("Clicked element: %s", locator)
                return  # Success

            except ElementClickInterceptedException:
                logger.info(
                    "[Retry %s]Click intercepted, attempting JS click fallback", attempt + 1
                )
                try:
                    driver.execute_script("arguments[0].click();", element)
                    return
                except Exception as js_error:
                    print(f"JS click failed: {js_error}")
                    time.sleep(1)

        raise Exception(
            f"Failed to click element after {retries} attempts: {locator}")

    @classmethod
    def wait_and_find_element(cls, locator):
        """
        Waits for a web element to become clickable and returns it.

        This function uses WebDriverWait to poll the DOM until the specified
        element is clickable, within a predefined timeout period. It is useful
        for ensuring that dynamic elements are interactable before performing
        actions.

        Parameters:
            locator (tuple): A tuple specifying the strategy to locate the
                            element, e.g., (By.ID, "submit-button").
        Returns:
            WebElement: The Selenium WebElement once it becomes clickable.

        Raises:
            TimeoutException: If the element does not become clickable within
                                the timeout.
        """
        driver = WebDriverManager.get_driver()
        elem = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable(locator))
        logger.debug("Element found and clickable: %s", locator)
        # Scroll element into view
        cls.scroll_to_element(elem)
        logger.debug("Scrolled to element: %s", locator)
        return elem

    @classmethod
    def wait_and_find_elements(cls, locator):
        """
        Waits for all elements matching the locator to be present in the DOM
        and returns them.

        This function uses WebDriverWait to wait until all elements specified
        by the locator are present in the DOM. It does not guarantee that the
        elements are visible or clickable, only that they exist in the page
        structure.

        Parameters:
            locator (tuple): (
                A tuple specifying the strategy to locate the elements,
                e.g., (By.CLASS_NAME, "item-row").
            )

        Returns:
            list[WebElement]: A list of Selenium WebElements once they are
                located.

        Raises:
            TimeoutException: If the elements are not found within the
                timeout period.
        """
        driver = WebDriverManager.get_driver()
        elements = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_all_elements_located(locator)
        )
        return elements

    @classmethod
    def wait_for_first_match(cls, locators, timeout=10):
        """
        Waits for the first matching element among multiple locators.

        Args:
            locators (dict): Dictionary with keys as labels and
                                values as locator tuples.
            timeout (int): Maximum time to wait for any locator to appear.

        Returns:
            str: The key of the locator that appeared first, or
                    'none' if none appeared.
        """
        driver = WebDriverManager.get_driver()
        end_time = time.time() + timeout
        while time.time() < end_time:
            for key, locator in locators.items():
                try:
                    if driver.find_element(*locator).is_displayed():
                        return key
                except (NoSuchElementException, StaleElementReferenceException):
                    continue
            time.sleep(0.5)
        return "none"

    @classmethod
    def fill_fields(cls, field_data):
        """
        Fills multiple input fields based on provided (value, locator) pairs.

        Args:
            field_data (
                List[Tuple[str, selenium.webdriver.remote.webelement.WebElement]]
            ):
                A list of tuples containing input values and their
                corresponding locators.

        Raises:
            ValueError: If any input value is missing or locator is not found.
        """
        for value, locator in field_data:
            if not value:
                raise ValueError(f"Missing input for locator: {locator}")
            try:
                element = cls.wait_and_find_element(locator)
                cls.clear_field(element)
                element.send_keys(value)
                logger.debug("Filled field %s with value: %s", locator, value)
                cls.verify_field(value, element, locator, scroll=True)
            except Exception as e:
                logger.error("Failed to fill field %s: %s", locator, e)
                raise

    @classmethod
    def clear_field(cls, element):
        """
        Attempts to clear the value of a web input element using multiple
        strategies.

        This function is designed for robust input clearing in browser
        automation tasks.
        It sequentially applies the following methods until the input field is empty:
        1. Native `clear()` method.
        2. Simulated CTRL+A + BACKSPACE keystrokes.
        3. Simulated CTRL+A + DELETE keystrokes.
        4. JavaScript-based value reset with input and change event dispatch.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement):
                The input element to be cleared.

        Returns:
            None

        Raises:
            Prints an error message if all clearing strategies fail
            or an exception occurs.
        """
        driver = WebDriverManager.get_driver()
        cls.scroll_to_element(element)
        try:
            # Strategy 1: Try native clear()
            element.clear()
            if element.get_attribute("value") == "":
                return

            # Strategy 2: CTRL+A + BACKSPACE
            element.click()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
            if element.get_attribute("value") == "":
                return

            # Strategy 3: CTRL+A + DELETE
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            if element.get_attribute("value") == "":
                return

            # Strategy 4: JavaScript clear + input event
            driver.execute_script("arguments[0].value = '';", element)
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input'));")
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change'));")

        except Exception as e:
            logger.error("Failed to clear input: %s", e)

    @classmethod
    def verify_field(cls, expected_value, element, locator, scroll=False):
        """
        Validates that a given input field contains the expected value,
        optionally scrolling to it before verification.

        This function retrieves the current value of the specified input field
        and compares it against the expected value.
        If `scroll` is True, it ensures the element is scrolled into view
        before performing the check. Any mismatch or interaction failure is
        logged and raised as an exception.

        Args:
            expected_value (str): The value expected to be present in the
                input field.
            element (selenium.webdriver.remote.webelement.WebElement):
                The WebElement representing the input field.
            locator (str): A string identifier used for logging and error
                reporting (e.g., XPath or CSS selector).
            scroll (bool, optional): Whether to scroll to the element before
                verification. Defaults to False.

        Raises:
            AssertionError: If the actual field value does not match the
                expected value.
            Exception: If the element cannot be accessed or interacted
                with.

        Notes:
            Adds a 0.5-second delay after verification to allow for UI
                stabilization.
            Logs both successful and failed verification attempts for
                traceability.
        """

        try:
            if scroll:
                cls.scroll_to_element(element)
            actual_value = element.get_attribute("value")
            assert (
                actual_value == expected_value
            ), f"Value mismatch at {locator}: expected '{expected_value}', got '{actual_value}'"
            logger.debug("Verified field %s: value '%s' matched",
                         locator, actual_value)
        except AssertionError as ae:
            logger.error("Verification failed for field %s: %s", locator, ae)
            raise
        except Exception as e:
            logger.error("Error verifying field %s: %s", locator, e)
            raise

    @classmethod
    def scroll_to_element(cls, element):
        """
        Scrolls the specified web element into view and focuses it for interaction.

        This function uses both JavaScript and ActionChains to ensure the element
        is visible and centered in the viewport. It is especially useful for small
        screens or scrollable containers.

        Args:
            element (selenium.webdriver.remote.webelement.WebElement):
                The web element to scroll into view and focus.
        """
        driver = WebDriverManager.get_driver()
        try:
            # JavaScript scroll (centered)
            driver.execute_script(
                """
                arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
            """,
                element,
            )

            # Focus the element
            driver.execute_script("arguments[0].focus();", element)

            # ActionChains scroll (fallback or reinforcement)
            ActionChains(driver).scroll_to_element(element).perform()

            time.sleep(0.2)  # Allow time for UI to settle
        except Exception as e:
            logger.warning("Scroll to element %s failed: %s", element, e)

    @classmethod
    def dismiss_browser_popup(cls):
        """
        Sends an ESCAPE key press to the browser to dismiss native popups
        or overlays.

        This is useful for closing Chrome's password change prompts,
        autofill overlays, or other browser-level dialogs that are not
        part of the DOM.
        """
        driver = WebDriverManager.get_driver()
        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            logger.debug("Sent ESCAPE key to dismiss browser popup")
        except Exception as e:
            logger.warning("Failed to dismiss popup with ESCAPE key: %s", e)
