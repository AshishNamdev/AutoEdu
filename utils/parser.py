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
Last Modified: 2025-09-04

Version: 1.0.0
"""

import json
import os

import pandas as pd

from common.logger import logger
from common.utils import backup_file, clean_column_name

import pandas as pd
from pandas import Timestamp
from dateutil.parser import parse

def load_and_clean_excel(path):
    """   
    Load an Excel file as a DataFrame with all values as strings, 
    replacing missing values and datetime placeholders with 'na', 
    and normalizing string content by stripping whitespace and
    and format valid dates to 'DD/MM/YYYY'
    """
    df = pd.read_excel(path, dtype=str)

    def clean_cell(x, col):
        if pd.isna(x):
            return "na"
        elif col.lower().__contains__("class"):
            return str(x)
        elif isinstance(x, Timestamp):
            return x.strftime("%d/%m/%Y")
        elif isinstance(x, str):
            x = x.strip()
            if x.lower() in ["", "nan", "nat"]:
                return "na"
            try:
                # Try parsing string as date
                dt = parse(x, dayfirst=True, fuzzy=False)
                return dt.strftime("%d/%m/%Y")
            except Exception:
                return x
        else:
            return str(x)

    # Apply cleaning column-wise
    # df = df.applymap(clean_cell)
    # Apply cleaning column-wise
    for col in df.columns:
        df[col] = df[col].apply(lambda x: clean_cell(x, col))
    
    df = df.fillna("na").replace("NaT", "na")
    return df


class StudentImportDataParser:
    """
    Parses and manages student import data for automation workflows.

    This class loads structured student data, backs up any existing JSON file,
    and serializes the parsed data for downstream use.
    It is designed to be extendable for dynamic data sources and integrates
    with file backup utilities.

    Attributes:
        import_data_file (str): Optional path to the raw import file.
        data_json_file (str): Path to the output JSON file.
        import_data (dict): Parsed student data keyed by PEN number.
    """

    def __init__(self, import_data_file=None):
        """
        Initializes the parser and prepares the output JSON file.

        If an existing `import_data.json` file is found in the current working
        directory, it is backed up and removed to ensure a clean write.

        Args:
            import_data_file (str, optional): Path to the raw import file.
        """
        if import_data_file is None:
            import_data_file = os.path.join(
                os.getcwd(), "input", "udise", "import_data.xlsx"
            )
        data_json_file = os.path.join(
            os.getcwd(), "input", "udise", "import_data.json"
        )
        if not os.path.exists(import_data_file):
            raise FileNotFoundError(
                f"Excel file not found: {import_data_file}")

        # Check if Student Import Data JSON already exists and backup it
        if os.path.exists(data_json_file):
            backup_file(data_json_file)
            os.remove(data_json_file)

        self.import_data_file = import_data_file
        self.data_json_file = data_json_file
        self.import_data = {}

    def parse_data(self):
        """
        Loads hardcoded student import data into memory.

        This method populates `self.import_data` with sample student records
        keyed by PEN number. It is intended as a placeholder for dynamic parsing
        from external sources in future implementations.

        Side Effects:
            - Updates `self.import_data`
            - Triggers serialization via `save_parsed_data_json()`
        """
        # Read Excel file into DataFrame
        df = load_and_clean_excel(self.import_data_file)
        
        # Clean column names
        df.columns = [clean_column_name(str(col)) for col in df.columns]

        # Ensure first column exists
        first_col = df.columns[0]

        na_count = 1

        # Build dictionary
        import_data = {}
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

            import_data[main_key] = sub_dict

        self.import_data = import_data
        logger.debug("✅ Data successfully parsed from %s",
                     self.import_data_file)
        self.save_parsed_data_json(df)

    def get_import_data(self):
        """
        Returns the parsed student import data.

        Returns:
            dict: Parsed student records keyed by PEN number.
        """

        return self.import_data

    def save_parsed_data_json(self, df):
        """
        Serializes the parsed import data and writes it to a JSON file.

        This method saves the contents of `self.import_data` to the file
        path specified by `self.data_json_file`, using UTF-8 encoding and
        pretty-print formatting for readability. Unicode characters are
        preserved in their original form.
        If the target directory does not exist, it is created.

        Raises:
            TypeError: If `self.import_data` contains non-serializable objects.
            FileNotFoundError: If the target directory does not exist.
            IOError: For general I/O errors during file writing.
        """
        if not os.path.exists(os.path.dirname(self.data_json_file)):
            os.makedirs(os.path.dirname(self.data_json_file), exist_ok=True)

        with open(self.data_json_file, "w", encoding="utf-8") as f:
            json.dump(self.import_data, f, indent=4, ensure_ascii=False)

        logger.info(
            "✅ Data successfully parsed and saved to %s", self.data_json_file)


class StudentProgressionDataParser:
    pass
