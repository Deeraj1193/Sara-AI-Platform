# backend/memory/memory_utils.py

def sanitize_text(text: str) -> str:
    """Basic cleanup before saving memory."""
    return text.strip()

def should_store_memory(user_input: str) -> bool:
    """Detect memory-worthy sentences."""
    lower = user_input.lower()
    if user_input.endswith("?"):
        return False
    return any(k in lower for k in [" i ", " my ", " im ", " i'm ", " me "])
