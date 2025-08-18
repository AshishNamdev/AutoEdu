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

# Path to the config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "conf.json")

# Load JSON config
with open(CONFIG_PATH, "r") as f:
    _config = json.load(f)

# Constants
PORTAL = _config["PORTAL"]

CLASS = _config["CLASS"]
SECTION = _config["SECTION"]
SECTIONS = _config["SECTIONS"]

# Nested options as constants
MODULE = _config[PORTAL]["MODULE"]
TASK = _config[PORTAL]["TASK"]
USERNAME = _config[PORTAL]["USERNAME"]
PASSWORD = _config[PORTAL]["PASSWORD"]
URL = _config[PORTAL][MODULE]["URL"] if PORTAL.lower() == "udise" else _config[PORTAL]["URL"]

TIMEOUT = _config["OPTIONS"]["timeout"]
VERIFY_SSL = _config["OPTIONS"]["verify_ssl"]
RETRIES = _config["OPTIONS"]["retries"]
