"""
Configures centralized logging for the automation framework.

This module sets up both console and rotating file logging using Python's
`logging.config.dictConfig`. It supports configurable log levels via environment
variables and ensures consistent formatting across all log outputs.

Author: Ashish Namdev (ashish28.sirt@gmail.com)
Date Created: 2025-08-18
Last Modified: 2025-08-18
Version: 1.0.0

Environment Variables:
    LOG_LEVEL (str): Optional. Sets the logging level (e.g., DEBUG, INFO, WARNING).

Attributes:
    logger (logging.Logger): Logger instance scoped to the current module.
"""

import logging
import logging.config
import os

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": os.getenv("LOG_LEVEL", "INFO")
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "autoedu.log",
            "maxBytes": 5_242_880,
            "backupCount": 3
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": os.getenv("LOG_LEVEL", "INFO")
    }
}

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
