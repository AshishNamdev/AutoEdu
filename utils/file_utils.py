"""
File backup utility for timestamped archival.

This module provides a function to create timestamped backups of files,
preserving metadata and ensuring traceability. It is useful for workflows
involving data versioning, audit trails, or recovery checkpoints.

Functions:
    - backup_file: Copies a source file into a backup directory with a
      timestamped filename.

Notes:
    - Uses microsecond-level timestamps for uniqueness.
    - Ensures backup directory exists before writing.
    - Logs both source and destination paths for traceability.
    
Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-08-23
Last Modified: 2025-09-22

Version: 1.0.0
"""

import os
import shutil

from common.logger import logger
from utils.date_time_utils import get_timestamp


def backup_file(src_path, backup_dir="backup"):
    """
    Creates a timestamped backup of the given file in the specified
    backup directory.

    Args:
        src_path (str): Path to the source file to back up.
        backup_dir (str): Directory where the backup will be stored.
                            Defaults to 'backup'.

    Returns:
        str: Full path to the created backup file.

    Raises:
        IOError: If backup fails due to permission or disk issues.
    """
    if not os.path.isfile(src_path):
        logger.error("Source file not found: %s", src_path)
        return

    os.makedirs(backup_dir, exist_ok=True)

    base_name = os.path.basename(src_path)
    name, ext = os.path.splitext(base_name)
    timestamp = get_timestamp()  # Includes microseconds
    backup_name = f"{name}_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)

    logger.info("%s --> %s", src_path, backup_path)
    shutil.copy2(src_path, backup_path)  # Preserves metadata
    return backup_path
    return backup_path
