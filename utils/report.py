"""
Module: student_import_report

This module provides functionality to generate an Excel report from
student import data.
It flattens a dictionary of student records keyed by PEN number,
applies a predefined column schema, and exports the data to a
structured Excel file with headers.

Features:
- Backs up existing report file before overwriting
- Enforces consistent column order using STUDENT_IMPORT_COLUMNS
- Handles missing fields gracefully (filled as NaN)
- Logs report generation status and file path

Intended for use in UDISE student import workflows where remarks and metadata
need to be preserved and exported for audit or review.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-08-23
Last Modified: 2025-08-23

Version: 1.0.1
"""

import os

import pandas as pd

from common.logger import logger
from common.utils import backup_file


def save_student_import_report(import_data):
    """
    Converts the import_data dictionary into a DataFrame and exports
    it to Excel with column headers defined in this method

    Args:
        import_data (dict): Dictionary containing student data keyed
                            by PEN number.

    Returns:
        None
    """
    # config.py or inside your report module
    STUDENT_IMPORT_COLUMNS = [
        "Student PEN",
        "Class",
        "Section",
        "Name",
        "Father Name",
        "Mother Name",
        "DOB",
        "Adhaar No.",
        "Adhaar Name",
        "Adhaar DOB" "Remark",
    ]

    report_file = os.path.join(os.getcwd(), "udise_student_import_report.xlsx")

    if os.path.exists(report_file):
        backup_file(report_file)
        os.remove(report_file)

    # Flatten the dictionary into a list of records
    report_rows = []
    for pen_no, data in import_data.items():
        row = {"Student PEN": pen_no}
        row.update(data)
        report_rows.append(row)

    # Create DataFrame and enforce column order
    df = pd.DataFrame(report_rows)
    df = df.reindex(columns=STUDENT_IMPORT_COLUMNS)  # Missing keys will be NaN
    df.to_excel(report_file, index=False)

    logger.info("Saved report to %s", report_file)
