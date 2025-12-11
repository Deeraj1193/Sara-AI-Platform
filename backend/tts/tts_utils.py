# backend/tts/tts_utils.py
"""
Utility helpers for TTS operations.
Will be expanded when real Kokoro functions move here.
"""

def save_audio_to_file(audio_bytes: bytes, path: str):
    """
    Placeholder file saver.
    """
    with open(path, "wb") as f:
        f.write(audio_bytes)
