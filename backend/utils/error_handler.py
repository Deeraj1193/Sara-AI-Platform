# backend/utils/error_handler.py
"""
Centralized error handling utilities.
Will be expanded later in Version 1.5 stability tasks.
"""

def safe_call(fn, *args, **kwargs):
    """
    Run a function safely.
    If it throws, return None instead of crashing the pipeline.
    """
    try:
        return fn(*args, **kwargs)
    except Exception:
        return None
