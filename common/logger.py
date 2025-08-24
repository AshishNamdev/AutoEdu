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
Last Modified: 2025-08-25

Version: 1.0.1
"""

import logging
import logging.config
import os

from common.time_utils import get_timestamp

log_dir = os.path.join(os.getcwd(), "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

timestamp = get_timestamp()
log_file = os.path.join(log_dir, f"auto_edu_{timestamp}.log")

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
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": log_file,
            "maxBytes": 5_242_880,
            "backupCount": 3,
            "level": "DEBUG",
        },
    },
    "loggers": {
        "auto_edu": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
    "root": {"handlers": ["console", "file"], "level": "INFO"},
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
