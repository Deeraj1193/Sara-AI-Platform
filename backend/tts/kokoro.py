# backend/tts/kokoro.py
"""
Kokoro TTS placeholder wrapper.
Actual Kokoro integration will be moved here later.
"""

class KokoroTTS:
    def __init__(self, config=None):
        self.config = config

    def synthesize(self, text: str):
        """
        Placeholder TTS output.
        Returns empty bytes for now.
        """
        return b""
