"""
student_data_parser.py

This module provides classes for parsing and managing student import data
used in educational automation workflows. It includes functionality to:

- Load and structure raw student data
- Backup and overwrite existing JSON files
- Serialize parsed data for downstream consumption

Classes:
    - StudentImportDataParser: Parses and stores student import data.
    - StudentProgressionDataParser: Placeholder for future progression logic.

Dependencies:
    - json
    - os
    - common.backup_file: Utility to backup existing files before overwrite.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created:  2025-08-21
Last Modified: 2025-09-22

Version: 1.0.0
"""

import json
import os
import re

import pandas as pd

from common.logger import logger
from utils.date_time_utils import get_timestamp
from utils.file_utils import backup_file
from utils.labels import clean_column_labels


def load_and_clean_excel(path):
    """
    Loads an Excel file and cleans it:
    - Converts all values to strings
    - Normalizes missing values to 'na'
    - Formats valid dates to 'DD/MM/YYYY'
    """
    df = pd.read_excel(path)

    def clean_cell(x, col):
        if pd.isna(x):
            return "na"
        if "class" in col.lower():
            return str(x)
        if isinstance(x, pd.Timestamp):
            return x.strftime("%d/%m/%Y")
        if isinstance(x, float):
            if x.is_integer():
                return str(int(x))
            return str(x)
        if isinstance(x, str):
            x = x.strip()
            x = re.sub(r"(?i)\b(?:mr|mrs)\b\.?\s*", "", x).strip()
            if x.lower() in ["", "nan", "nat"]:
                return "na"
            try:
                dt = pd.to_datetime(x, dayfirst=True, errors="raise")
                return dt.strftime("%d/%m/%Y")
            except Exception:
                return x
        return str(x)

    for col in df.columns:
        df[col] = df[col].apply(lambda x: clean_cell(x, col))
    return df


class StudentDataParser:
    """
    Parses and manages student import data for automation workflows.

    This class loads structured student data, backs up any existing JSON file,
    and serializes the parsed data for downstream use.
    It is designed to be extendable for dynamic data sources and integrates
    with file backup utilities.

    Attributes:
        data_json_file (str): Path to the output JSON file.
        student_data (dict): Parsed student data keyed by PEN number.
    """

    def __init__(self, student_data_file):
        """
        Initializes the parser and prepares the output JSON file.

        If an existing `student_data.json` file is found in the current working
        directory, it is backed up and removed to ensure a clean write.

        Args:
            student_data_file (str, optional): Path to the raw import file.
        """
        if not os.path.exists(student_data_file):
            raise FileNotFoundError(
                f"Excel file not found: {student_data_file}")

        data_json_file = student_data_file.replace(".xlsx", ".json")

        # Check if Student Import Data JSON already exists and backup it
        if os.path.exists(data_json_file):
            backup_file(data_json_file)
            os.remove(data_json_file)

        self.student_data_file = student_data_file
        self.data_json_file = data_json_file
        self.parsed_data = {}

    def parse_data(self):
        """
        Loads hardcoded student data into memory.

        This method populates `self.student_data` with sample student records
        keyed by PEN number. It is intended as a placeholder for dynamic parsing
        from external sources in future implementations.

        Side Effects:
            - Updates `self.student_data`
            - Triggers serialization via `save_parsed_data_json()`
        """
        # Read Excel file into DataFrame
        df = load_and_clean_excel(self.student_data_file)

        # Clean column names
        df.columns = [clean_column_labels(str(col)) for col in df.columns]

        # Ensure first column exists
        first_col = df.columns[0]

        na_count = 1

        # Build dictionary
        parsed_data = {}
        for _, row in df.iterrows():
            main_key = str(row[first_col]).strip()

            if main_key.strip().lower() == "na":
                main_key = f"NA_{na_count}"
                na_count += 1
            # if not main_key:
            #    continue  # Skip rows with empty first cell

            # Create sub-dictionary excluding the first column
            sub_dict = {}
            for col in df.columns[1:]:  # Skip first column
                value = row[col]
                if isinstance(value, pd.Timestamp):
                    sub_dict[col] = value.strftime("%Y-%m-%d")
                else:
                    sub_dict[col] = value

            parsed_data[main_key] = sub_dict

        self.parsed_data = parsed_data
        logger.debug("Data successfully parsed from %s",
                     self.student_data_file)
        self._save_parsed_data_json(df)

    def get_parsed_data(self):
        """
        Returns the parsed student data.

        Returns:
            dict: Parsed student records dictionary.
        """

        return self.parsed_data

    def update_parsed_data(self, main_key, kwargs):
        """
        Updates the parsed data for a specific student identified
        by Main Key.

        This method modifies the `parsed_data` dictionary by setting the
        specified `key` to the provided `value` for the student with the
        given `main_key`. If the `main_key` does not exist in the dictionary,
        it logs a warning message.

        Args:
            pen_no (str): The main_key of the student whose data
                            is to be updated.
            kwargs (dict): The key and value to add in  student's
                            data dictionary.

        Returns:
            None

        Side Effects:
            - Modifies the `parsed_data` attribute of the class instance.
            - Logs a warning if the specified PEN number is not found.
        """
        if main_key in self.parsed_data:
            for key, value in kwargs.items():
                self.parsed_data[main_key][key] = value
                logger.debug("Updated %s: %s - %s", main_key, key, value)
            self.parsed_data[main_key]["Date and Time"] = get_timestamp(
                format="%d-%m-%Y - %I:%M:%S %p")
        else:
            logger.warning("%s not found in parsed data. No update made.",
                           main_key)

    def _save_parsed_data_json(self, df):
        """
        Serializes the parsed import data and writes it to a JSON file.

        This method saves the contents of `self.student_data` to the file
        path specified by `self.data_json_file`, using UTF-8 encoding and
        pretty-print formatting for readability. Unicode characters are
        preserved in their original form.
        If the target directory does not exist, it is created.

        Raises:
            TypeError: If `self.student_data` contains non-serializable objects.
            FileNotFoundError: If the target directory does not exist.
            IOError: For general I/O errors during file writing.
        """
        if not os.path.exists(os.path.dirname(self.data_json_file)):
            os.makedirs(os.path.dirname(self.data_json_file), exist_ok=True)

        with open(self.data_json_file, "w", encoding="utf-8") as f:
            json.dump(self.parsed_data, f, indent=4, ensure_ascii=False)

        logger.info(
            "Data successfully parsed and saved to %s", self.data_json_file)


class StudentProgressionDataParser:
    pass
