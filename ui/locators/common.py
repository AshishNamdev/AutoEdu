"""
main_page_locator.py

Provides Selenium locator definitions for the main page of the portal.

This module defines structured locator tuples used in UI automation scripts to
identify and interact with key elements on the portal's landing page. It references
selector constants from `MainPageSelector` to ensure consistency and reduce duplication
across the automation framework.

Classes:
    MainPageLocator: Contains locator tuples for validating page load and detecting
                    server-side errors such as HTTP 503.

Dependencies:
    - selenium.webdriver.common.by.By
    - ui.selectors.common.MainPageSelector

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-20
Last Modified: 2025-08-20

Version: 1.0.0
"""

from ui.selectors.common import MainPageSelector
from selenium.webdriver.common.by import By


class MainPageLocator:
    """
    Defines locator tuples for elements on the main page.

    This class centralizes Selenium locator definitions to support maintainable
    and readable UI automation. It references selector constants from
    `MainPageSelector` to ensure consistency and reduce duplication.

    Attributes:
        BODY (tuple): Locator for the <body> tag, used to detect page-level errors
                        or confirm successful page load.
    """

    BODY = (By.TAG_NAME, MainPageSelector.BODY_TAG)
