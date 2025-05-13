# src/debugonce/decorator.py
import functools
import inspect
import json
import os
import sys
import traceback
from datetime import datetime

def debugonce(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            capture_state(func, args, kwargs, result)
            return result
        except Exception as e:
            capture_state(func, args, kwargs, exception=e)
            raise

    return wrapper

def capture_state(func, args, kwargs, result=None, exception=None):
    state = {
        "function": func.__name__,
        "args": list(args),  # Convert args to a list
        "kwargs": kwargs,
        "result": result,
        "exception": str(exception) if exception else None,
        "environment_variables": dict(os.environ),
        "current_working_directory": os.getcwd(),
        "python_version": sys.version,
        "timestamp": datetime.now().isoformat()
    }

    if exception:
        state["stack_trace"] = traceback.format_exc()

    save_state(state)

def save_state(state):
    # Save the state to a file
    with open("debugonce.json", "w") as f:
        json.dump(state, f, indent=4)