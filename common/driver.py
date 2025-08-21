"""
Initializes and configures the Selenium WebDriver for Chrome.

This module sets up a Chrome WebDriver instance using `webdriver-manager` to
automatically handle driver installation. It also configures the browser to
remain open after script execution by enabling the 'detach' option.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-08-22

Version: 1.0.1

Attributes:
    driver (webdriver.Chrome): A configured instance of Chrome WebDriver.
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from common.logger import logger


def get_chrome_service(driver_path=False):
    if driver_path:
        path = os.path.join(os.getcwd(), "driver", "chrome", "chromedriver.exe")
        # logger.info("Starting Chrome with %s driver", path)
    else:
        path = ChromeDriverManager().install()
    return Service(path)


# Setup WebDriver
options = Options()
options.add_experimental_option("detach", True)

try:
    service = get_chrome_service()
except Exception:
    # logger.exception("AutoEdu encountered an error: %s", str(e))
    service = get_chrome_service(driver_path=True)
driver = webdriver.Chrome(service=service, options=options)
