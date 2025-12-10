# Sara AI — Local Assistant (v1.0)

Sara AI is a fully local personal assistant featuring:
- FastAPI backend with persona and memory logic  
- Local LLM text generation (via Ollama)  
- Long-term memory system (SQLite)  
- Kokoro-based TTS with audio playback  
- Modern React/Vite frontend  

Sara is designed for experimentation, personalization, and offline use.

---

## 🌟 Features (v1.0)

- **Local text generation**  
  Powered by a local Ollama model (Gemma 3 1B by default).

- **Persona engine**  
  Modes: *Gremlin*, *Teaching*, *Professional*  
  Toggles: *Child Mode, Emojis, Formal Tone*  
  Sliders: *Swear level, Roast level, Verbosity, Spontaneity*

- **Long-term memory**  
  Automatically saves user facts and retrieves relevant context.

- **High-quality local TTS (Kokoro)**  
  Generates `.wav` per message, served via FastAPI static routes.

- **Refined React UI**  
  - Chat bubbles with Markdown + code highlighting  
  - Persona editor  
  - Memory viewer  
  - Notes panel  
  - Smooth animations & glass UI styling

---

## 🧱 Architecture Overview

```

Frontend (React)
├── Chat UI (ChatBubble, InputBar)
├── Persona Panel
├── Memory Panel
└── saraApi.js → calls backend

Backend (FastAPI)
├── server.py → REST endpoints
├── brain.py → LLM prompt, persona logic, memory retrieval
├── tts/kokoro_tts.py → audio generation
└── scripts/memory.py → SQLite memory DB

Local Runtime
├── Ollama (text model)
└── Kokoro (TTS)

```

---

## 🧠 Memory System

Sara extracts and stores structured information automatically:

- **“My name is X”** → relation  
- **“I like Y”** → preference  
- **“I am Z”** → identity  
- Other statements → generic fact  

Everything appears in the Memory tab of the UI and is reused during conversations.

---

## 🎙️ TTS System (Kokoro)

Sara uses **Kokoro 82M** locally to synthesize audio.  
Each reply results in a `.wav` written to:

```

backend/audio_cache/

```

The backend returns an accessible URL such as:

```

/audio/tts_sara_1700000000.wav

````

The frontend automatically preloads and plays the audio.

---

## 🧩 API Summary

### **POST /api/chat**
Returns Sara’s text + audio:

```json
{
  "reply": "Hello!",
  "audio_url": "/audio/tts_sara_170000.wav",
  "memory_update": false
}
````

### **POST /api/tts**

Arbitrary text-to-speech:

Input:

```json
{ "text": "Hello!", "speed": 1.0 }
```

Output:

```json
{ "audio_url": "/audio/tts_custom_170000.wav" }
```

### **GET /api/persona**, **POST /api/persona**

Synchronizes persona configuration with the frontend.

### **GET /api/memory**

Returns long-term memory entries.

---

## 📂 Folder Structure

```
SaraAI/
│── backend/
│   ├── server.py
│   ├── brain.py
│   ├── persona_store.py
│   ├── scripts/memory.py
│   └── tts/kokoro_tts.py
│
│── frontend/
│   ├── src/api/saraApi.js
│   ├── components/
│   ├── layout/
│   └── assets/
│
│── README.md
```

---

## 🖼️ Screenshots 

## UI Preview
<img width="1918" height="857" alt="image" src="https://github.com/user-attachments/assets/66743cdd-9d64-4362-871f-395e5a622cd6" />

---

## 🚀 Roadmap

### **v1.0 — COMPLETE**

Core conversation, persona, memory, TTS, and full UI.

### **v1.5 — Next**

* Voice presets and tuning
* Latency optimization
* Modularized TTS backend
* UI improvements

### **v2.0 — Future**

* Talking Mode (continuous speech)
* Live subtitles
* Multi-profile support
* Plugin ecosystem

---

## ⚠️ Notes

* This assistant is meant for *local personal use only*.
* No install steps included by design.


---

