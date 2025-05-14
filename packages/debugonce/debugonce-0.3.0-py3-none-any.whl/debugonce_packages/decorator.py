# src/debugonce/decorator.py
import functools
import inspect
import json
import os
import sys
import traceback
from datetime import datetime
import builtins  # To override the built-in open function

def debugonce(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Capture the original open function
        original_open = builtins.open
        file_access_log = []


        # Define a custom open function to track file access
        def custom_open(file, mode='r', *args, **kwargs):
            filepath = os.path.abspath(file)
            if not filepath.startswith(os.path.abspath(".debugonce")):
                operation = "read" if "r" in mode else "write"
                file_access_log.append({"file": filepath, "operation": operation})
            return original_open(file, mode, *args, **kwargs)

        # Replace the built-in open function with the custom one
        builtins.open = custom_open

        try:
            # Execute the function and capture the result
            result = func(*args, **kwargs)
            capture_state(func, args, kwargs, result, file_access_log=file_access_log)
            return result
        except Exception as e:
            # Capture the state in case of an exception
            capture_state(func, args, kwargs, exception=e, file_access_log=file_access_log)
            raise
        finally:
            # Restore the original open function
            builtins.open = original_open

    return wrapper

def capture_state(func, args, kwargs, result=None, exception=None, file_access_log=None):
    state = {
        "function": func.__name__,
        "args": list(args),  # Convert args to a list
        "kwargs": kwargs,
        "result": result,
        "exception": str(exception) if exception else None,
        "environment_variables": dict(os.environ),
        "current_working_directory": os.getcwd(),
        "python_version": sys.version,
        "timestamp": datetime.now().isoformat(),
        "file_access": file_access_log or []  # Add file access log
    }

    if exception:
        state["stack_trace"] = traceback.format_exc()

    # Temporarily restore the original open function to avoid logging save_state operations
    original_open = builtins.open
    save_state(state)
    builtins.open = original_open

def save_state(state):
    # Save the state to a file
    os.makedirs(".debugonce", exist_ok=True)
    file_path = os.path.join(".debugonce", f"session_{int(datetime.now().timestamp())}.json")
    with open(file_path, "w") as f:
        json.dump(state, f, indent=4)