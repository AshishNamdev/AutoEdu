"""
Configures centralized logging for the automation framework.

This module sets up both console and rotating file logging using Python's
`logging.config.dictConfig`. It supports configurable log levels via environment
variables and ensures consistent formatting across all log outputs.

Environment Variables:
    LOG_LEVEL (str): Optional. Sets the logging level (e.g., DEBUG, INFO, WARNING).

Attributes:
    logger (logging.Logger): Logger instance scoped to the current module.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-08-20

Version: 1.0.0
"""

from datetime import datetime
import logging
import logging.config
import os

log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)


LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(module)s:%(lineno)d (%(funcName)s) - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": os.getenv("LOG_LEVEL", "INFO"),
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": os.path.join("logs", "auto_edu.log"),
            "maxBytes": 5_242_880,
            "backupCount": 3,
        },
    },
    "root": {"handlers": ["console", "file"], "level": os.getenv("LOG_LEVEL", "INFO")},
}

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("auto_edu")


def get_timestamp():
    """
    Returns the current timestamp formatted for log entries.

    Format:
        DD-MM-YYYY - HH:MMAM/PM (e.g., "20-08-2025 - 03:45PM")

    Returns:
        str: A string representing the current date and time.
    """

    return datetime.now().strftime("%d-%m-%Y - %I:%M:%Sp")


def log_start():
    """
    Logs the start of the AutoEdu automation run with a timestamp.

    Output Format:
        =========== Starting AutoEdu [DD-MM-YYYY - HH:MMAM/PM] =========

    Uses:
        - get_timestamp() to generate the current time.
        - logger.info() to write the entry to the shared log file.
    """

    logger.info("=========== Starting AutoEdu [%s] =========", get_timestamp())


def log_end():
    """
    Logs the end of the AutoEdu automation run with a timestamp.

    Output Format:
        =========== End AutoEdu [DD-MM-YYYY - HH:MMAM/PM] =========

    Uses:
        - get_timestamp() to generate the current time.
        - logger.info() to write the entry to the shared log file.
    """

    logger.info("=========== End AutoEdu [%s] =========", get_timestamp())


log_start()
