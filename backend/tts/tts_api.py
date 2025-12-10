# tts_api.py
from .kokoro_tts import synthesize_tts

def generate_sara_voice(text: str, speed: float = 1.0):
    """
    Frontend-friendly wrapper.
    Calls Kokoro TTS, returns audio file path.
    """
    try:
        path = synthesize_tts(text=text, speed=speed)
        return {"status": "ok", "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e)}
