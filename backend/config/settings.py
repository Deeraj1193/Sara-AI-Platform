# backend/config/settings.py
"""
Central configuration loader.
Keeps all environment variables and default settings in one place.
"""

import os

class Settings:
    def __init__(self):
        # Basic environment mode
        self.ENV = os.getenv("ENV", "development")

        # Placeholder values (expand later)
        self.MODEL_PATH = os.getenv("MODEL_PATH", "./models")
        self.MEMORY_DB = os.getenv("MEMORY_DB", "./sara_memory.db")
        self.TTS_VOICE = os.getenv("TTS_VOICE", "kokoro_default")

settings = Settings()
