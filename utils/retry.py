import time
from functools import wraps


def retry_on_exception(exception_type, retries=3, delay=1):
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
