# Sara AI — Local Assistant (v1.5)

Sara AI is a fully local personal assistant featuring:
- FastAPI backend with modularized pipeline, persona, routing, and memory engines  
- Local LLM text generation (via Ollama)  
- Long-term memory (SQLite)  
- Kokoro TTS (local)  
- Modern React/Vite frontend  

Version **1.5** introduces a complete backend rewrite and modular architecture to support future upgrades (v2.0, v2.5, v3.5+).

---

## 🌟 Features (v1.5)

### 🔧 **Modular Backend Architecture**
A fully refactored backend using clean modules for:
- Pipeline  
- Router  
- Memory system  
- Persona system  
- TTS  
- Multiple LLM wrappers  

### 🤹 **Multi-Model Routing**
Sara now automatically selects between specialized models:
- **Casual model**  
- **Coding model**  
- **Teaching model**  
- **Fast-talking model** (short latency replies)

### 🧠 **Improved Long-term Memory**
- Uses `MemoryManager` and `memory_utils`  
- Structured memory formatting  
- Injects relevant context into model prompts  
- Memory panel UI works identically

### 🧬 **Enhanced Persona Engine**
Modes:
- Gremlin  
- Teaching  
- Professional  

Toggles:
- Child Mode  
- Emojis  
- Formal Tone  

Sliders:
- Swear level  
- Roast level  
- Verbosity  
- Spontaneity  

All persona filters are applied to **any** model automatically.

### 🎙️ **Kokoro TTS Integrated Cleanly**
- Stable audio caching
- Accessible audio URLs
- Ready for future “Talking Mode” upgrades

### 💎 **Stable & Clean Frontend**
Frontend required **no changes** for v1.5.  
It remains fully compatible with the new backend.

---

## 🧱 Architecture Overview (v1.5)

```md
Frontend (React)
├── Chat UI (ChatBubble, InputBar)
├── Persona Panel
├── Memory Panel
└── saraApi.js → backend calls

Backend (FastAPI, Modular)
├── core/
│   ├── pipeline.py          → Central orchestrator
│   ├── sara_router.py       → Model routing logic
│   └── sara_persona.py      → Persona engine
│
├── models/
│   ├── local_casual.py
│   ├── local_coding.py
│   ├── local_teaching.py
│   └── fast_talking.py
│
├── memory/
│   ├── memory_core.py
│   └── memory_utils.py
│
├── tts/
│   └── kokoro_tts.py
│
├── persona_store.py
└── server.py → REST endpoints

Local Runtime
├── Ollama (LLM)
└── Kokoro (TTS)
````

---

## 🧠 Memory System (v1.5)

Sara automatically extracts and stores structured facts:

* “My name is X” → **relation**
* “I like Y” → **preference**
* “I am Z” → **identity**
* Other things → **generic fact**

Memory is fetched and injected into model prompts.

---

## 🎙️ TTS System (Kokoro)

Sara uses **Kokoro 82M** locally to generate `.wav` files stored in:

```
backend/audio_cache/
```

The backend returns URLs like:

```
/audio/tts_<unique>.wav
```

Frontend auto-plays the audio.

---

## 🧩 API Summary

### **POST /api/chat**

Returns text + audio:

```json
{
  "reply": "Hello!",
  "audio_url": "/audio/tts_170000.wav",
  "memory_update": false,
  "model_used": "local_casual"
}
```

### **POST /api/chat_stream**

Text streaming endpoint.

### **POST /api/tts**

Free-form TTS generation.

### **GET/POST /api/persona**

Persona sync.

### **GET /api/memory**

Full memory list.

---

## 📂 Folder Structure (v1.5)

```
SaraAI/
│── backend/
│   ├── core/
│   ├── models/
│   ├── memory/
│   ├── tts/
│   ├── persona_store.py
│   ├── server.py
│   └── __init__.py
│
│── frontend/
│   ├── src/
│   └── assets/
│
│── system_prompt.txt
│── few_shot_examples.txt
│── README.md
```

---

## 🚀 Roadmap (official from project document)

This README references the project roadmap file for exact milestone definitions (see project docs). Summary below:

* **v1.0 — Core local assistant** (foundation)
* **v1.5 — Stability & multi-model routing** (this release)
* **v2.0 — Cloud deployment & portfolio demo** (move backend to cloud, hosted DB, secure demo)
* **v2.5 — Advanced utilities (web scraping + video editing)** (hybrid features, heavy-job pods)
* **v3.0 — System testing & optimization (stress testing)** (load tests, profiling, reliability)
* **v3.5 — PNG avatar & UI redesign** (static avatar + emotion variants)
* **v4.0 — Live2D integration & streaming (VTuber)** (rigging, mouth-sync, OBS integration)

(Full roadmap sourced from project roadmap file.) 

---

## ⚠️ Notes

* This assistant is for **local personal use**.
* No installation script is included by design.

```

---

I updated the roadmap to match your uploaded roadmap exactly and added the citation so anyone reading the README knows the source. :contentReference[oaicite:2]{index=2}

Next step if you want to finalize the release:

- I can provide the exact git commands to commit README and push the v1.5 tag.
- Or I can make a small CHANGELOG.md (optional).

Say one of:

- **“commit and tag v1.5”** — I’ll give the git commands and a commit message.
- **“make CHANGELOG.md and commit”** — I’ll provide changelog content and the commands.
- **“not yet”** — I’ll wait.
```

