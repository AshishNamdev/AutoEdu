"""
Initializes and configures the Selenium WebDriver for Chrome.

This module sets up a Chrome WebDriver instance using `webdriver-manager` to
automatically handle driver installation. It also configures the browser to
remain open after script execution by enabling the 'detach' option.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-18
Last Modified: 2025-08-18
Version: 1.0.0

Attributes:
    driver (webdriver.Chrome): A configured instance of Chrome WebDriver.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
