"""
Loads configuration constants from a JSON file for use across the automation framework.

This module reads `conf.json` located in the same directory and exposes key settings
as constants, including credentials, URLs, class/section identifiers, and nested options
like timeout and retry behavior.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-18
Last Modified: 2025-08-18
Version: 1.0.0

Attributes:
    USERNAME (str): Login username.
    PASSWORD (str): Login password.
    URL (str): Target URL for browser automation.
    CLASS (str): Class identifier.
    SECTION (str): Section identifier.
    SECTIONS (list): List of available sections.
    TIMEOUT (int): Timeout value for WebDriver waits.
    VERIFY_SSL (bool): Flag to enable/disable SSL verification.
    RETRIES (int): Number of retry attempts for operations.
"""

import json
import os

from .logger import logger

# Path to the config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "conf.json")

# Load JSON config
with open(CONFIG_PATH, "r") as f:
    _config = json.load(f)

PORTAL = _config["PORTAL"]
CLASS = _config["CLASS"]
SECTION = _config["SECTION"]
SECTIONS = _config["SECTIONS"]

# Derived values
MODULE = _config["MODULE"][PORTAL]
TASK = _config["TASK"][PORTAL][MODULE]
USERNAME = _config["USERNAME"][PORTAL]
PASSWORD = _config["PASSWORD"][PORTAL]

# URL handling
if PORTAL == "udise":
    URL = _config["URL"][PORTAL][MODULE]
else:
    URL = _config["URL"][PORTAL]


# Options
TIMEOUT = _config["OPTIONS"]["timeout"]
TIME_DELAY = _config["OPTIONS"]["time_delay"]
VERIFY_SSL = _config["OPTIONS"]["verify_ssl"]
RETRIES = _config["OPTIONS"]["retries"]
VERIFY_SSL = _config["OPTIONS"]["verify_ssl"]
RETRIES = _config["OPTIONS"]["retries"]

logger.info("=================== Start AutoEdu ===================")
logger.info("CONFIG_PATH: %s", CONFIG_PATH)
logger.info("PORTAL: %s", PORTAL)
logger.info("MODULE: %s", MODULE)
logger.info("TASK: %s", TASK)
logger.info("URL: %s", URL)
logger.info("TIMEOUT: %s", TIMEOUT)
logger.info("TIME_DELAY: %s", TIME_DELAY)
