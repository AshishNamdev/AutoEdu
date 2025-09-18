"""
Manages and configures Selenium WebDriver instances for multiple browsers.

Supports Chrome, Firefox, and Edge with automatic driver installation via
`webdriver-manager`. Provides a singleton-style `get_driver()` method for
reuse across modules.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-18
Last Modified: 2025-09-18
Version: 2.0.0
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from common.config import DEBUG


class WebDriverManager:
    _driver = None

    @classmethod
    def _get_service(cls, browser, force_local=False):
        """
        Resolves the appropriate driver service based on browser type.

        Args:
            browser (str): One of 'chrome', 'firefox', 'edge'.
            force_local (bool): If True, forces use of local driver path.

        Returns:
            Service: Selenium WebDriver service object.
        """
        use_local = DEBUG or force_local
        cwd = os.getcwd()

        if browser == "chrome":
            path = (
                os.path.join(cwd, "driver", "chrome", "chromedriver.exe")
                if use_local else ChromeDriverManager().install()
            )
            return ChromeService(path)

        if browser == "firefox":
            path = (
                os.path.join(cwd, "driver", "firefox", "geckodriver.exe")
                if use_local else GeckoDriverManager().install()
            )
            return FirefoxService(path)

        if browser == "edge":
            path = (
                os.path.join(cwd, "driver", "edge", "msedgedriver.exe")
                if use_local else EdgeChromiumDriverManager().install()
            )
            return EdgeService(path)

        raise ValueError(f"Unsupported browser: {browser}")

    @classmethod
    def _get_options(cls, browser):
        """
        Returns browser-specific options.

        Args:
            browser (str): One of 'chrome', 'firefox', 'edge'.

        Returns:
            Options: Selenium browser options object.
        """
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            })
            options.add_experimental_option("detach", True)
            return options

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("detach", True)
            return options

        elif browser == "edge":
            options = webdriver.EdgeOptions()
            # options.use_chromium = True
            options.add_experimental_option("detach", True)
            return options

        raise ValueError(f"Unsupported browser: {browser}")

    @classmethod
    def get_driver(cls, browser="chrome"):
        """
        Returns a singleton WebDriver instance for the specified browser.

        Args:
            browser (str): One of 'chrome', 'firefox', 'edge'.

        Returns:
            WebDriver: Selenium WebDriver instance.
        """
        if cls._driver is None:
            try:
                service = cls._get_service(browser)
            except Exception:
                service = cls._get_service(browser, force_local=True)

            options = cls._get_options(browser)

            if browser == "chrome":
                cls._driver = webdriver.Chrome(service=service, options=options)
            elif browser == "firefox":
                cls._driver = webdriver.Firefox(service=service, options=options)
            elif browser == "edge":
                cls._driver = webdriver.Edge(service=service, options=options)

        return cls._driver
