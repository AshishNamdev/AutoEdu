"""
__init__.py

Initializes the UI automation package and exposes key components.

This module defines the `MainPage` class, which provides health check utilities
for validating portal availability and detecting server-side errors (e.g., HTTP 503).
It also imports shared configuration, locators, and logging utilities.

Classes:
    MainPage: Performs status checks on the portal's main page after browser launch.

Dependencies:
    - selenium.common.exceptions.TimeoutException
    - common.config.URL
    - ui.locators.common.MainPageLocator
    - common.driver
    - common.logger

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-20
Last Modified: 2025-08-20

Version: 1.0.0
"""

from selenium.common.exceptions import TimeoutException
from common.config import URL
from ui.locators.common import MainPageLocator
from common import driver
from common.logger import logger


class MainPage:
    """
    Represents the main landing page of an educational portal.

    This class provides utility methods to validate the availability and status
    of the main page after browser launch. It is primarily used to detect
    server-side errors such as HTTP 503 and log appropriate diagnostics.

    Intended for use in portal health checks and pre-test validations.
    """

    @staticmethod
    def check_status(url=URL):
        """
        Checks the status of the main page after browser launch.

        This method waits for the page to load and inspects the body text
        for indicators of a 503 Service Unavailable error. If detected,
        it logs the error with context. Otherwise, it confirms successful page load.

        Args:
            url (str): The URL of the portal's main page.

        Logs:
            - Error if "503 Service Unavailable" or related message is found.
            - Info if the page loads successfully.
            - Exception details for timeouts or unexpected failures.
        """

        try:
            # Wait for page to load and check for 503 indicators
            body_text = driver.find_element(*MainPageLocator.BODY).text
            if (
                "503 Service Unavailable" in body_text
                or "No server is available" in body_text
            ):
                logger.error("Error: %s at %s", body_text, url)
                logger.info("Shutting down browser driver and terminating AutoEdu session.")
                driver.quit()
                exit()
            else:
                logger.info("Page loaded successfully: %s", driver.title)
        except TimeoutException:
            logger.exception("Timeout while loading page: %s", url)
        except Exception as e:
            logger.exception("Unexpected error after browser launch: %s", str(e))
