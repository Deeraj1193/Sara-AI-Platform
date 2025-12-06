# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .brain import generate_reply, generate_stream, list_all_memories
from .persona_store import get_persona, set_persona

app = FastAPI(title="Sara API")

# ----------------------------------------------------------
# CORS SETTINGS (keep yours)
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


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# ----------------------------------------------------------
# Persona GET/POST (keeps UI <-> backend sync)
# ----------------------------------------------------------
@app.get("/api/persona")
async def api_get_persona():
    return get_persona()


@app.post("/api/persona")
async def api_set_persona(cfg: dict):
    # Accepts full persona JSON from frontend
    set_persona(cfg)
    return {"status": "ok"}


# ----------------------------------------------------------
# NON-STREAMING CHAT (used by your current frontend sendMessage)
# ----------------------------------------------------------
@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    reply, memory_flag = generate_reply(req.message)
    return {"reply": reply, "memory_update": memory_flag}


# ----------------------------------------------------------
# STREAMING CHAT (kept for later; not required by current UI)
# ----------------------------------------------------------
@app.post("/api/chat_stream")
async def chat_stream(req: ChatRequest):
    token_generator, memory_flag = generate_stream(req.message)

    async def event_stream():
        try:
            for token in token_generator:
                yield token
        finally:
            yield ""

    return StreamingResponse(event_stream(), media_type="text/plain")


# ----------------------------------------------------------
# MEMORY ENDPOINT
# ----------------------------------------------------------
@app.get("/api/memory")
async def api_memory():
    items = list_all_memories()
    return {"items": [{"id": i, "text": t} for i, t in items]}


@app.get("/")
async def root():
    return {"status": "Sara API running"}
