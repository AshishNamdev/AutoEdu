"""
Manages and configures Selenium WebDriver instances for multiple browsers.

Supports Chrome, Firefox, and Edge with automatic driver installation via
`webdriver-manager`. Provides a singleton-style `get_driver()` method for
reuse across modules.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)
Date Created: 2025-08-18
Last Modified: 2025-10-15
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

from common.config import BROWSER, DEBUG


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

        service_map = {
            "chrome": lambda: ChromeService(
                os.path.join(cwd, "driver", "chrome", "chromedriver.exe")
                if use_local else ChromeDriverManager().install()
            ),
            "firefox": lambda: FirefoxService(
                os.path.join(cwd, "driver", "firefox", "geckodriver.exe")
                if use_local else GeckoDriverManager().install()
            ),
            "edge": lambda: EdgeService(
                os.path.join(cwd, "driver", "edge", "msedgedriver.exe")
                if use_local else EdgeChromiumDriverManager().install()
            ),
        }

        try:
            return service_map[browser]()
        except KeyError:
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

        if browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("detach", True)
            return options

        if browser == "edge":
            options = webdriver.EdgeOptions()
            # options.use_chromium = True
            options.add_experimental_option("detach", True)
            return options

        raise ValueError(f"Unsupported browser: {browser}")

    @classmethod
    def get_driver(cls):
        """
        Returns a singleton WebDriver instance for the specified browser.

        Returns:
            WebDriver: Selenium WebDriver instance.
        """
        if cls._driver is None:
            try:
                service = cls._get_service(BROWSER)
            except Exception:
                service = cls._get_service(BROWSER, force_local=True)

            options = cls._get_options(BROWSER)

            # Mapping of browser names to their corresponding
            # WebDriver constructors
            driver_map = {
                "chrome": lambda: webdriver.Chrome(service=service, options=options),
                "firefox": lambda: webdriver.Firefox(service=service, options=options),
                "edge": lambda: webdriver.Edge(service=service, options=options),
            }

            # Fallback to chrome if browser is not in the map
            cls._driver = driver_map.get(BROWSER, driver_map["chrome"])()

        return cls._driver
