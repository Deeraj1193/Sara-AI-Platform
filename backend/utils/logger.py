# backend/utils/logger.py
"""
Simple logger utility.
Other modules can import get_logger() to log safely.
"""

import logging

def get_logger(name: str = "sara"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Basic console output
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
