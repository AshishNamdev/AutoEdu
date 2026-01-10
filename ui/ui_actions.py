"""
Provides a reusable, resilient UIActions class for interacting with
web elements using Selenium.

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
    from ui.ui_actions import UIActions as UI

    UI.fill_fields({
        (By.ID, "username"): "admin",
        (By.ID, "password"): "secret"
    })

Intended for use in AutoEdu workflows and other scalable automation platforms.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2026-01-10

Version: 1.0.0
"""

import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.config import TIMEOUT
from common.driver import WebDriverManager
from common.logger import logger


class UIActions:
    """
    Utility class for resilient, reusable UI automation actions.

    This class provides a suite of static interaction methods designed to:
    - Abstract common Selenium operations like clicking, locating,
        and filling fields
    - Handle dynamic UI behavior with retries, scrolling, and popup dismissal
    - Support robust automation pipelines with fallback logic and traceable
        actions

    Methods:
        wait_and_click(locator, retries=2):
            Waits for an element to be clickable and clicks it,
            retrying if necessary.

        wait_and_find_element(locator):
            Waits for a single element to be present and returns it.

        wait_and_find_elements(locator):
            Waits for multiple elements matching the locator and returns them.

        wait_for_first_match(locators, timeout=10):
            Waits for the first matching locator from a list and returns
            the element.

        fill_fields(field_data):
            Fills multiple fields using a dictionary of locator-value pairs.

        clear_field(element):
            Clears the content of a given input field element.

        verify_field(expected_value, element, locator, scroll=False):
            Verifies that a field contains the expected value, optionally
            scrolling to it.

        scroll_to_element(element):
            Scrolls the page to bring the specified element into view.

        dismiss_browser_popup():
            Attempts to dismiss any active browser alert or popup.

    Usage:
        UIActions.wait_and_click(locator)
        UIActions.fill_fields((username, StudentLoginLocators.USERNAME))
    """

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
    def wait_and_find_element(cls, locator, parent_element=None):
        """
        Waits for a web element to become clickable and returns it.

        This function uses WebDriverWait to poll the DOM until the specified
        element is clickable, within a predefined timeout period. It is useful
        for ensuring that dynamic elements are interactable before performing
        actions.

        Parameters:
            locator (tuple): A tuple specifying the strategy to locate the
                            element, e.g., (By.ID, "submit-button").
            parent_element (WebElement, optional): Parent element to search
                            within. Defaults to None.
        Returns:
            WebElement: The Selenium WebElement once it becomes clickable.

        Raises:
            TimeoutException: If the element does not become clickable within
                                the timeout.
        """
        driver = (
            parent_element
            if parent_element
            else WebDriverManager.get_driver()
        )
        elem = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable(locator))
        logger.debug("Element found and clickable: %s", locator)
        # Scroll element into view
        cls.scroll_to_element(elem)
        logger.debug("Scrolled to element: %s", locator)
        return elem

    @classmethod
    def wait_and_find_elements(cls, locator, parent_element=None):
        """
        Wait until all elements matching the locator are present in the DOM.

        This does not guarantee that the elements are visible or clickable,
        only that they exist in the page structure.

        Args:
            locator (tuple): A tuple specifying the strategy to locate the
                elements, e.g., (By.CLASS_NAME, "item-row").
            parent_element (WebElement, optional): Parent element to search
                within. Defaults to None.

        Returns:
            list[WebElement]: A list of Selenium WebElements once located.

        Raises:
            TimeoutException: If the elements are not found within the timeout.
        """
        driver = (
            parent_element
            if parent_element
            else WebDriverManager.get_driver()
        )

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
                        logger.debug("Found %s:%s", *locator)
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

    @staticmethod
    def wait_until_ready(locator, timeout: int = 10, parent: WebElement = None):
        """
        Wait until the given element is present and clickable.

        Args:
            locator (tuple): A locator tuple (By.<method>, "selector").
            timeout (int): Maximum time to wait in seconds. Default is 10.
            parent (WebElement, optional): Parent element to search within.
                                            Defaults to None.

        Returns:
            WebElement: The element once it is ready.

        Raises:
            TimeoutException: If the element is not ready within the timeout.
        """
        try:
            # assumes UI.driver is your WebDriver instance
            driver = parent if parent else WebDriverManager.get_driver()
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error("Element %s not ready within %s seconds",
                         locator, timeout)
            raise
