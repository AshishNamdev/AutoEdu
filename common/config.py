"""
Loads configuration constants from a JSON file for use across the automation
framework.

This module reads `conf.json` located in the same directory and exposes
key settings as constants, including credentials, URLs,
class/section identifiers, and nested options like timeout and retry behavior.
It also provides a utility function to log these configurations for debugging
purposes.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-10-15

Version: 1.0.0

Attributes:
    CONFIG_PATH (str): Absolute path to the conf.json file.
    _config (dict): Parsed JSON configuration dictionary.

    DEBUG (bool): Enables debug mode for verbose logging. Default is False.
    SUPPORTED_BROWSERS (list): List of supported browser names.
    BROWSER (str): Selected browser.
                    Defaults to "edge", falls back to "chrome" if unsupported.

    PORTAL (str): Target portal name (e.g., "udise").
    CLASS (str): Target class for student import. Default is "9".
    SECTION (str): Target section for student import. Default is "A".
    SECTIONS (dict): Mapping of section labels to internal codes.

    MODULE (str): Active module for the selected portal. Defaults to "student".
    TASK (str): Task type for the portal/module. Defaults to "import".
    USERNAME (str): Username for portal login. Defaults to "default_user".
    PASSWORD (str): Password for portal login. Defaults to "default_password".

    URL (str): Target URL for the selected portal and module.

    TIMEOUT (int): Timeout duration in seconds for UI waits. Default is 30.
    TIME_DELAY (float): Delay between UI actions in seconds. Default is 1.0.
    VERIFY_SSL (bool): Whether to verify SSL certificates. Default is True.
    RETRIES (int): Number of retry attempts for UI actions. Default is 3.

    CLASS_AGE_MAP (dict): Mapping of class to expected age for YOB inference.
    MAX_YOB_TRIAL_RANGE (int): Maximum number of YOB trials allowed.
                                Default is 3
"""

import json
import os

# Path to the config file
CONFIG_PATH = os.path.join(os.getcwd(), "conf.json")


# Load JSON config
with open(CONFIG_PATH, "r") as f:
    _config = json.load(f)

DEBUG = _config.get("DEBUG", False)
SUPPORTED_BROWSERS = _config.get("SUPPORTED_BROWSERS")
BROWSER = _config.get("BROWSER", "edge")
BROWSER = BROWSER if BROWSER in SUPPORTED_BROWSERS else "chrome"

PORTAL = _config.get("PORTAL", "udise")
CLASS = _config.get("CLASS", "9")
SECTION = _config.get("SECTION", "A")
SECTIONS = _config.get("SECTIONS",
                       {"A": "1", "B": "2", "C": "3",
                        "D": "4", "E": "5", "F": "6"}
                       )

# Derived values
MODULE = _config.get("MODULE", {}).get(PORTAL, "student")
TASK = _config.get("TASK", {}).get(PORTAL, {}).get(MODULE, "import")
USERNAME = _config.get("USERNAME", {}).get(PORTAL, "default_user")
PASSWORD = _config.get("PASSWORD", {}).get(PORTAL, "default_password")

# URL handling
if PORTAL == "udise":
    URL = _config.get("URL", {}).get(PORTAL, {}).get(MODULE, "default_url")
else:
    URL = _config.get("URL", {}).get(PORTAL, "default_url")

# Options
TIMEOUT = _config.get("OPTIONS", {}).get("timeout", 30)
TIME_DELAY = float(_config.get("OPTIONS", {}).get("time_delay", 1))
VERIFY_SSL = _config.get("OPTIONS", {}).get("verify_ssl", True)
RETRIES = _config.get("OPTIONS", {}).get("retries", 3)

CLASS_AGE_MAP = _config.get("CLASS_AGE_MAP")
MAX_YOB_TRIAL_RANGE = _config.get("MAX_YOB_TRIAL_RANGE", 3)


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

    logger.debug("DEBUG: %s", DEBUG)
    logger.debug("CONFIG_PATH: %s", CONFIG_PATH)
    logger.info("PORTAL: %s", PORTAL)
    logger.info("MODULE: %s", MODULE)
    logger.info("TASK: %s", TASK)
    logger.debug("URL: %s", URL)
    logger.debug("TIMEOUT: %s", TIMEOUT)
    logger.debug("TIME_DELAY: %s", TIME_DELAY)
