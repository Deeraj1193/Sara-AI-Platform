# backend/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# NEW Pipeline import (correct package path)
from backend.core.pipeline import Pipeline

# Persona store (still old system — OK until Step 31 cleanup)
from .persona_store import get_persona, set_persona

# Kokoro TTS (unchanged)
from .tts.kokoro_tts import kokoro

import base64
import os
from pathlib import Path


app = FastAPI(title="Sara API")
pipeline = Pipeline()


# ----------------------------------------------------------
# CORS SETTINGS
# ----------------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------
# AUDIO SETUP
# ----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio_cache"
AUDIO_DIR.mkdir(exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# ----------------------------------------------------------
# PERSONA GET/POST
# ----------------------------------------------------------
@app.get("/api/persona")
async def api_get_persona():
    return get_persona()


@app.post("/api/persona")
async def api_set_persona(cfg: dict):
    set_persona(cfg)
    return {"status": "ok"}


# ----------------------------------------------------------
# SAVE WAV FROM BASE64
# ----------------------------------------------------------
def save_wav_base64(b64: str) -> str:
    raw = base64.b64decode(b64)
    fname = f"tts_{os.getpid()}_{len(raw)}.wav"
    fpath = AUDIO_DIR / fname
    with open(fpath, "wb") as f:
        f.write(raw)
    return fname


# ----------------------------------------------------------
# NON-STREAM CHAT
# ----------------------------------------------------------
@app.post("/api/chat")
async def api_chat(req: ChatRequest):

    result = pipeline.handle_message(req.message, req.session_id)
    reply = result["reply"]
    memory_flag = result["memory_update"]

    # TTS
    audio_url = None
    try:
        b64 = kokoro.synthesize_base64(reply, speed=1.0)
        fname = save_wav_base64(b64)
        audio_url = f"/audio/{fname}"
    except Exception:
        audio_url = None

    return {
        "reply": reply,
        "audio_url": audio_url,
        "memory_update": memory_flag,
        "model_used": result.get("model_used", "unknown"),
    }


# ----------------------------------------------------------
# TTS ONLY
# ----------------------------------------------------------
@app.post("/api/tts")
async def api_tts(payload: dict):
    text = payload.get("text", "")
    speed = float(payload.get("speed", 1.0))

    if not text:
        return {"error": "Missing 'text' field"}

    try:
        b64 = kokoro.synthesize_base64(text, speed=speed)
        fname = save_wav_base64(b64)
        return {"audio_url": f"/audio/{fname}"}
    except Exception as e:
        return {"error": str(e)}


# ----------------------------------------------------------
# STREAM CHAT ENDPOINT
# ----------------------------------------------------------
@app.post("/api/chat_stream")
async def chat_stream(req: ChatRequest):

    token_generator, memory_flag = pipeline.handle_stream(
        req.message, req.session_id
    )

    async def event_stream():
        try:
            for token in token_generator:
                yield token
        finally:
            yield ""

    return StreamingResponse(event_stream(), media_type="text/plain")


# ----------------------------------------------------------
# ROOT CHECK
# ----------------------------------------------------------
@app.get("/")
async def root():
    return {"status": "Sara API running"}
