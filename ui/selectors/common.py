"""
main_page_selectors.py

Provides selector constants for identifying elements on the main page of the portal.

This module is part of the locator architecture used in UI automation. It defines
semantic identifiers for HTML elements to promote readability, consistency, and
ease of maintenance across test scripts and page object models.

Classes:
    MainPageSelector: Contains tag-based selectors for key elements on the main page.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-20
Last Modified: 2025-08-20

Version: 1.0.0
"""


class MainPageSelector:
    """
    Contains locator constants for elements on the main page.

    This class centralizes selector definitions to support maintainable and readable
    automation scripts. Useful for identifying key elements during page validation,
    error detection, and UI interactions.

    Attributes:
        BODY_TAG
    """

    BODY_TAG = "body"
