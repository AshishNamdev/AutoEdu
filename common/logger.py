"""
Centralized logging configuration for the AutoEdu automation framework.

This module sets up consistent logging across the framework using Python's
`logging.config.dictConfig`. It supports both console and rotating
file handlers, ensures uniform formatting, and dynamically creates a
timestamped log file within a dedicated `logs/` directory.

Features:
    - Console and file logging with rotation (5MB max, 3 backups)
    - Dynamic log level based on DEBUG flag from config
    - Timestamped log filenames for traceability
    - Utility functions to log the start and end of automation runs

Attributes:
    logger (logging.Logger): Logger instance scoped to the 'auto_edu'
                            namespace.

Author:
    Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Created: 2025-08-18
Last Modified: 2025-10-03

Version: 1.0.0
"""


import logging
import logging.config
import os

from common.config import DEBUG
from utils.date_time_utils import get_timestamp

log_dir = os.path.join(os.getcwd(), "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

timestamp = get_timestamp()
log_file = os.path.join(log_dir, f"auto_edu_{timestamp}.log")
log_level = "DEBUG" if DEBUG else "INFO"

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
            "level": log_level,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": log_file,
            "maxBytes": 5_242_880,
            "backupCount": 3,
            "level": log_level,
        },
    },
    "loggers": {
        "auto_edu": {
            "handlers": ["console", "file"],
            "level": log_level,
            "propagate": False,
        }
    },
    "root": {"handlers": ["console", "file"], "level": log_level},
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
