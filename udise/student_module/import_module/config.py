import json
import os

# Path to the config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "conf.json")

# Load JSON config
with open(CONFIG_PATH, "r") as f:
    _config = json.load(f)

# Constants
USERNAME = _config["USERNAME"]
PASSWORD = _config["PASSWORD"]
URL = _config["URL"]
CLASS = _config["CLASS"]
SECTION = _config["SECTION"]
SECTIONS = _config["SECTIONS"]

# Nested options as constants
TIMEOUT = _config["OPTIONS"]["timeout"]
VERIFY_SSL = _config["OPTIONS"]["verify_ssl"]
RETRIES = _config["OPTIONS"]["retries"]
