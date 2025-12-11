# 📜 CHANGELOG

All notable changes to **Sara AI** will be documented in this file.

This project follows a structured milestone roadmap:  
**v1.0 → v1.5 → v2.0 → v2.5 → v3.0 → v3.5 → v4.0**

---

## **[v1.5] — 2025-12-11**
### ⭐ Major Backend Modularization (Completed)

A full architectural rewrite enabling cloud migration, multi-model orchestration, and future advanced features.

### 🔧 Backend Architecture
- Introduced a fully modularized backend structure  
- Added `core/` (pipeline, router, persona engine)  
- Added `models/` (casual, coding, teaching, fast-talking)  
- Added `memory/` (`memory_core`, `memory_utils`)  
- Added `tts/` + modular Kokoro TTS wrapper  
- Removed old scripts (`brain.py`, legacy memory scripts)  
- Stable import paths & dependency cleanup  

### 🧠 Pipeline & Model Routing
- New central `Pipeline` orchestrator  
- Router selects the best model automatically  
- Unified `generate_reply()` and `generate_stream()` through model wrappers  

### 🧬 Persona Engine Upgrade
- Migrated to `core/sara_persona.py`  
- Supports modes: **gremlin**, **teaching**, **professional**  
- Supports toggles: **child mode**, **formal tone**, **emoji toggle**  
- Supports sliders: **swear level**, **verbosity**, **roast level**, **spontaneity**  
- Centralized persona post-filter system  

### 🧠 Memory Engine Rewrite
- Added `MemoryManager` and `memory_utils`  
- Cleaner memory formatting & relevance ranking  
- Proper memory injection into prompt pipeline  

### 🎙️ TTS Integration
- Modular Kokoro TTS wrapper  
- Safe model loading  
- Unified audio generation flow  
- Static audio caching under `/audio/`  

### 🖥️ Frontend Compatibility
- No UI changes required  
- Frontend automatically works with new backend  
- Ready for future cloud API adjustments  

---

## **[v1.0] — 2025-12-10**
### ⭐ Initial Release

A fully working local AI assistant featuring:

- Local LLM (Ollama + Gemma 3 1B)  
- Basic persona system  
- SQLite memory storage  
- Kokoro TTS integration  
- React/Vite chat UI  
- Memory viewer, persona panel, notes panel  
- Basic backend structure  

---

# 📅 **Future Roadmap**  

---

## **[v2.0] — Cloud Version**
- Deploy backend to cloud  
- Add authentication + environment configs  
- Route LLM + TTS through cloud APIs  
- Improve API stability & CORS  
- Prepare portfolio-ready demo instance  

---

## **[v2.5] — Advanced Features**
- Web scraping module  
- Video editing module (backend job runners / pods)  
- Expand memory formatting  
- Tool pipeline integration  

---

## **[v3.0] — Stress Testing**
- Load testing  
- Memory leak checks  
- CPU/GPU/RAM profiling  
- Latency benchmarking  
- Failover + stability tests  

---

## **[v3.5] — PNG Avatar UI**
- PNG-based character  
- Emotion-based expression engine  
- UI redesign for avatar + chat layout  

---

## **[v4.0] — Live2D Integration**
- Rigged Live2D model  
- TTS lip-sync  
- Expression blending  

---
