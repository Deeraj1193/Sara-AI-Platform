# backend/utils/text_utils.py
"""
General text utility helpers.
Real helpers will be added later.
"""

def normalize(text: str) -> str:
    return text.strip()

def truncate(text: str, max_len: int = 2000) -> str:
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text
