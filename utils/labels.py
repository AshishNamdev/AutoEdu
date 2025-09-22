"""
Label normalization utilities for schema hygiene and UI consistency.

This module provides reusable functions for transforming column labels and
special-case keys (e.g., 'NA_<number>') into standardized formats suitable for
JSON, Excel, and UI layers. It supports both normalization and restoration
flows to ensure round-trip compatibility between internal keys and user-facing
labels.

Functions:
    - clean_column_labels: Normalizes or restores column names for schema
                           alignment.
    - normalize_na_label: Resolves 'NA_<number>' variants to canonical
                           'NA' labels.

Use these utilities to enforce consistent naming conventions across data
pipelines, improve onboarding clarity, and reduce ambiguity in schema mappings.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-09-22

Version: 1.0.0
"""


import re


def clean_column_labels(column_name, restore=False):
    """
    Normalizes or restores column lables for consistent schema handling.

    This utility transforms column lables into a safe, JSON-compatible format
    by trimming whitespace, converting to lowercase, and replacing spaces with
    underscores.
    When `restore=True`, it restores the original display format
    by converting underscores to spaces and applying title casing.

    Args:
        column_name (str): The column name to be transformed.
        restore (bool, optional): If True, restores the transformation to
            produce a human-readable label. Defaults to False.

    Returns:
        str: A cleaned or restored column name,
            depending on the `restore` flag.

    Examples:
        clean_column_name("Student Name") → "student_name"
        clean_column_name("student_name", restore=True) → "Student Name"

    Notes:
        - Useful for mapping UI labels to internal keys and vice versa.
        - Ensures consistent naming across JSON, Excel, and UI layers.
    """
    return (
        column_name.strip().lower().replace(" ", "_")
        if not restore
        else column_name.strip().title().replace("_", " ")
    )


def normalize_na_label(input):
    """
    Normalizes 'NA_<number>' labels to 'NA'.

    If input is a dictionary, replaces keys matching 'NA_<number>' with 'NA'.
    If input is a string, replaces it directly if it matches the pattern.

    Args:
        input (str or dict): A string label or dictionary with string keys.

    Returns:
        str or dict: Normalized label or dictionary with cleaned keys.

    Example:
        >>> normalize_na_label("NA_42")
        'NA'
        >>> normalize_na_label({"NA_42": "x", "EU_99": "y"})
        {'NA': 'x', 'EU_99': 'y'}
    """
    pattern = r"^NA_\d+$"

    if isinstance(input, dict):
        return {
            re.sub(pattern, "NA", key)
            if re.match(pattern, key)
            else key: value
            for key, value in input.items()
        }

    if isinstance(input, str):
        return (
            re.sub(pattern, "NA", input)
            if re.match(pattern, input)
            else input
        )

    raise TypeError(f"Input {input} must be a str or dict[str, str]")
