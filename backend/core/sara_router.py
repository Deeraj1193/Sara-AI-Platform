# backend/core/sara_router.py

"""
Real routing logic for Sara AI Version 1.5.
Chooses the best model based on message intent.
"""

import re


def route_to_model(message_text: str, mode_hint: str = None) -> str:
    """
    Determine which model should handle the input.
    Order of checks:
    1. Mode hint override (Talking Mode / code-mode / teach-mode)
    2. Keyword-based intent detection
    3. Pattern classifiers
    4. Fallback: local_casual
    """

    text = message_text.lower().strip()

    # ------------------------------------
    # 1. MODE HINT OVERRIDE (optional)
    # ------------------------------------
    if mode_hint:
        return mode_hint

    # ------------------------------------
    # 2. FAST-TALKING MODE trigger
    # ------------------------------------
    # Used when TTS needs super quick replies
    short = len(text.split()) <= 4
    if short and any(k in text for k in ["hi", "hey", "yo", "ok", "yes", "no", "wait"]):
        return "fast_talking"

    # ------------------------------------
    # 3. CODING INTENT
    # ------------------------------------
    coding_keywords = [
        "code", "bug", "fix", "error", "compile", "function",
        "class", "python", "js", "java", "c++", "debug", "stack trace"
    ]
    if any(k in text for k in coding_keywords):
        return "local_coding"

    # ------------------------------------
    # 4. TEACHING / EXPLANATION INTENT
    # ------------------------------------
    teaching_patterns = [
        r"explain", r"teach", r"how does", r"what is", r"why does",
        r"break it down", r"step by step", r"make me understand"
    ]
    for p in teaching_patterns:
        if re.search(p, text):
            return "local_teaching"

    # ------------------------------------
    # 5. FALLBACK: CASUAL CONVERSATION
    # ------------------------------------
    return "local_casual"
