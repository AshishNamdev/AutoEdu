"""
Module: student_import_report

This module defines the `StudentImportReport` class, which encapsulates
the logic for generating structured Excel and JSON reports from student
import data keyed by PEN number.

Designed for UDISE workflows, it supports audit-friendly exports,
column schema enforcement, and automatic backup of previous reports.

Features:
- Converts nested student data into a flat tabular format
- Saves both JSON and Excel versions of the report
- Backs up existing report files before overwriting
- Enforces column order using a configurable schema
- Handles missing fields gracefully (filled as NaN)
- Logs report generation status and file path

Usage:
    from student_import_report import StudentImportReport
    report = StudentImportReport(import_data, column_order=STUDENT_IMPORT_COLUMNS)
    report.save()

Intended for integration into AutoEdu or similar automation platforms
where traceability, modularity, and user-friendly exports are critical.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-08-23
Last Modified: 2025-09-04

Version: 1.0.0
"""


import json
import os

import pandas as pd

from common.logger import logger
from common.utils import backup_file


class StudentImportReport:
    """
    Generates structured Excel and JSON reports from student import data.

    Features:
    - Backs up existing report files before overwriting
    - Enforces consistent column order using STUDENT_IMPORT_COLUMNS (if provided)
    - Handles missing fields gracefully
    - Logs report generation status and file path

    Intended for UDISE student import workflows.

    Author: Ashish Namdev
    Version: 1.0.1
    """

    def __init__(self, import_data, column_order=None):
        """
        Initializes the report generator with student data and configuration.

        Args:
            import_data (dict): Dictionary of student records keyed by PEN number.
            report_subdir (str): Subdirectory under 'reports' for saving files.
            column_order (list, optional): List of column names to enforce order.
        """
        self.import_data = import_data
        report_dir = os.path.join(os.getcwd(), "reports", "udise")
        self.report_json_file = os.path.join(report_dir, "import_report.json")
        self.report_excel_file = os.path.join(report_dir, "import_report.xlsx")
        self.column_order = column_order

        os.makedirs(report_dir, exist_ok=True)

    def _backup_existing_reports(self):
        """
        Backs up existing report files (JSON and Excel) before overwriting.

        Uses `backup_file()` utility and removes originals to ensure clean
        write.
        """
        for f in [self.report_json_file, self.report_excel_file]:
            if os.path.isfile(f):
                backup_file(f)
                os.remove(f)

    def _flatten_import_data(self):
        """
        Converts nested student dictionary into a flat list of row
        dictionaries.

        Each row includes 'Student PEN' and associated metadata.

        Returns:
            list[dict]: Flattened student records.
        """

        rows = []
        for pen_no, data in self.import_data.items():
            row = {"Student PEN": pen_no}
            if isinstance(data, dict):
                row.update(data)
            rows.append(row)
        return rows

    def _apply_column_order(self, df):
        """
        Reorders DataFrame columns based on the provided schema.

        Missing columns are added with NaN values. If no schema is provided,
        columns are sorted alphabetically.

        Args:
            df (pd.DataFrame): Raw DataFrame of student records.

        Returns:
            pd.DataFrame: Reordered DataFrame.
        """

        if self.column_order:
            # Fill missing columns with NaN
            for col in self.column_order:
                if col not in df.columns:
                    df[col] = pd.NA
            return df[self.column_order]
        else:
            return df[sorted(df.columns)]

    def save(self):
        """
        Generates and saves the student import report.

        - Backs up existing files
        - Saves raw data as JSON
        - Converts data to Excel with enforced column order
        - Logs the output path
        """

        self._backup_existing_reports()

        with open(self.report_json_file, "w", encoding="utf-8") as f:
            json.dump(self.import_data, f, indent=4, ensure_ascii=False)

        df = pd.DataFrame(self._flatten_import_data())
        df = self._apply_column_order(df)

        df.to_excel(self.report_excel_file, index=False)
        logger.info("Saved report to %s", self.report_excel_file)
