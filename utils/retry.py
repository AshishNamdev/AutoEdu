"""
Retry Decorator Utility for Exception Handling.

This module provides a reusable decorator `retry_on_exception` that wraps any function
and retries its execution upon encountering a specified exception type. It is useful
for automating resilience in flaky operations such as network requests, UI interactions,
or file I/O.

Features:
    - Configurable number of retries and delay between attempts.
    - Exception-specific retry logic.
    - Preserves original function metadata using `functools.wraps`.

Example:
    @retry_on_exception(ValueError, retries=5, delay=2)
    def fragile_function():
        ...

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-18
Last Modified: 2025-08-20

Version: 1.0.0
"""

import time
from functools import wraps


def retry_on_exception(exception_type, retries=3, delay=1):
    """
    Decorator to retry a function upon encountering a specific exception.

    Args:
        exception_type (Exception): The exception type to catch and retry on.
        retries (int, optional): Number of retry attempts. Defaults to 3.
        delay (int or float, optional): Delay in seconds between retries. Defaults to 1.

    Returns:
        function: A wrapped function that will retry on the specified exception.

    Raises:
        exception_type: If all retry attempts fail, the exception is re-raised.

    Example:
        @retry_on_exception(ConnectionError, retries=5, delay=2)
        def fetch_data():
            ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exception_type as e:
                    print(f"[Retry {attempt+1}] {func.__name__} failed: {e}")
                    time.sleep(delay)
            raise exception_type(f"{func.__name__} failed after {retries} retries.")

        return wrapper

    return decorator
