"""
Loads configuration constants from a JSON file for use across the automation framework.

This module reads `conf.json` located in the same directory and exposes key settings
as constants, including credentials, URLs, class/section identifiers, and nested options
like timeout and retry behavior.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-08-24

Version: 1.0.1

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

# Path to the config file
CONFIG_PATH = os.path.join(os.getcwd(), "conf.json")


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
TIME_DELAY = float(_config["OPTIONS"]["time_delay"])
VERIFY_SSL = _config["OPTIONS"]["verify_ssl"]
RETRIES = _config["OPTIONS"]["retries"]
VERIFY_SSL = _config["OPTIONS"]["verify_ssl"]
RETRIES = _config["OPTIONS"]["retries"]


def log_config(logger):
    """
    Logs key configuration parameters used in the automation suite.

    This function records the current values of global configuration variables
    such as paths, portal identifiers, module names, task types, URLs, and
    timeout settings. It is typically called at the start of execution to
    provide visibility into the runtime environment and aid in debugging.

    Logged parameters:
        - CONFIG_PATH: Path to the configuration file.
        - PORTAL: Identifier for the target portal.
        - MODULE: Name of the module being executed.
        - TASK: Type of task being performed.
        - URL: Target URL for automation.
        - TIMEOUT: Maximum wait time for operations.
        - TIME_DELAY: Delay between actions or retries.
    """

    logger.debug("CONFIG_PATH: %s", CONFIG_PATH)
    logger.debug("PORTAL: %s", PORTAL)
    logger.debug("MODULE: %s", MODULE)
    logger.debug("TASK: %s", TASK)
    logger.debug("URL: %s", URL)
    logger.debug("TIMEOUT: %s", TIMEOUT)
    logger.debug("TIME_DELAY: %s", TIME_DELAY)
