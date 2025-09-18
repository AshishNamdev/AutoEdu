"""
Utility functions for Selenium-based browser automation.

This module provides helper functions to wait for elements,
and perform robust clicking actions with retry logic.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-09-19

Version: 1.0.0

Functions:
    - wait_and_find_element(locator): Waits for a single clickable element.
    - wait_and_find_elements(locator): Waits for multiple elements to be
                                       present.
    - wait_and_click(locator, retries): Scrolls to and clicks an element with
                                        retry fallback.
"""

import os
import random
import re
import shutil
import time
from datetime import datetime, timedelta

from dateutil import parser
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
from common.logger import logger
from common.time_utils import get_timestamp


# -------------------- UI Interaction Class --------------------
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

# -------------------- Standalone Utility Functions --------------------


def backup_file(src_path, backup_dir="backup"):
    """
    Creates a timestamped backup of the given file in the specified
    backup directory.

    Args:
        src_path (str): Path to the source file to back up.
        backup_dir (str): Directory where the backup will be stored.
                            Defaults to 'backup'.

    Returns:
        str: Full path to the created backup file.

    Raises:
        IOError: If backup fails due to permission or disk issues.
    """
    if not os.path.isfile(src_path):
        logger.error("Source file not found: %s", src_path)
        return

    os.makedirs(backup_dir, exist_ok=True)

    base_name = os.path.basename(src_path)
    name, ext = os.path.splitext(base_name)
    timestamp = get_timestamp()  # Includes microseconds
    backup_name = f"{name}_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)

    logger.info("%s --> %s", src_path, backup_path)
    shutil.copy2(src_path, backup_path)  # Preserves metadata
    return backup_path


def convert_to_ddmmyyyy(date_str):
    """
    Converts a date string to DD/MM/YYYY format, intelligently detecting format.

    Args:
        date_str (str): Input date string.

    Returns:
        str: Date formatted as "DD/MM/YYYY".
    """
    try:
        # Normalize input
        date_str = date_str.strip().lower()
        date_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)

        # Match numeric formats like DD/MM/YYYY or MM/DD/YYYY
        numeric_match = re.match(
            r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$", date_str)
        if numeric_match:
            first, second, year = map(int, numeric_match.groups())
            # If first > 12, it's definitely the day
            if first > 12:
                day, month = first, second
            # If second > 12, it's definitely the month
            elif second > 12:
                day, month = second, first
            else:
                # Ambiguous: default to DD/MM/YYYY
                day, month = first, second
            return f"{day:02d}/{month:02d}/{year}"

        # Fallback to parser with dayfirst=True for natural language
        parsed_date = parser.parse(date_str, dayfirst=True)
        return parsed_date.strftime("%d/%m/%Y")

    except Exception as e:
        raise ValueError(f"Invalid date format: {date_str}") from e


def clean_column_labels(column_name, restore=False):
    """
    Normalizes or restores column lables for consistent schema handling.

    This utility transforms column lables into a safe, JSON-compatible format
    by trimming whitespace, converting to lowercase, and replacing spaces with
    underscores.
    When `restore=True`, it restores the original display format
    by converting underscores to spaces and applying title casing.

    Args:
        column_name (str): The column name to be transformed.
        restore (bool, optional): If True, restores the transformation to
            produce a human-readable label. Defaults to False.

    Returns:
        str: A cleaned or restored column name,
            depending on the `restore` flag.

    Examples:
        clean_column_name("Student Name") → "student_name"
        clean_column_name("student_name", restore=True) → "Student Name"

    Notes:
        - Useful for mapping UI labels to internal keys and vice versa.
        - Ensures consistent naming across JSON, Excel, and UI layers.
    """
    return (
        column_name.strip().lower().replace(" ", "_")
        if not restore
        else column_name.strip().title().replace("_", " ")
    )


def random_date(start_date, end_date, date_format):
    """
    Generate a random date between start_date and end_date.

    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format (default).
        end_date (str): End date in 'YYYY-MM-DD' format (default).
        date_format (str): Format of input/output dates.

    Returns:
        str: Random date in the same format.
    """
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    delta = end - start
    random_days = random.randint(0, delta.days)
    result = start + timedelta(days=random_days)
    return result.strftime(date_format)
