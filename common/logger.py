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
Last Modified: 2025-08-22

Version: 1.0.1
"""

import logging
import logging.config
import os

from common.time_utils import get_timestamp

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


def log_start():
    """
    Logs the start of the AutoEdu automation run with a timestamp.

    Output Format:
        =========== Starting AutoEdu [DD-MM-YYYY - HH:MMAM/PM] =========

    Uses:
        - get_timestamp() to generate the current time.
        - logger.info() to write the entry to the shared log file.
    """

    logger.info(
        "=========== Starting AutoEdu [%s] =========",
        get_timestamp(format="%d-%m-%Y - %I:%M:%S %p"),
    )


def log_end():
    """
    Logs the end of the AutoEdu automation run with a timestamp.

    Output Format:
        =========== End AutoEdu [DD-MM-YYYY - HH:MMAM/PM] =========

    Uses:
        - get_timestamp() to generate the current time.
        - logger.info() to write the entry to the shared log file.
    """

    logger.info(
        "=========== End AutoEdu [%s] =========",
        get_timestamp(format="%d-%m-%Y - %I:%M:%S %p"),
    )


log_start()
