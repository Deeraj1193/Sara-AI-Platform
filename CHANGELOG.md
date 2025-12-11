📜 CHANGELOG

All notable changes to Sara AI will be documented in this file.

This project follows a structured milestone roadmap:
v1.0 → v1.5 → v2.0 → v2.5 → v3.0 → v3.5 → v4.0

[v1.5] — 2025-12-11
Major Backend Modularization (Completed)

A full architectural rewrite enabling cloud migration, multi-model orchestration, and future advanced features.

🔧 Backend Architecture

Introduced a fully modularized backend structure

Added core/ (pipeline, router, persona engine)

Added models/ (casual, coding, teaching, fast-talking)

Added memory/ (memory_core, memory_utils)

Added tts/ + modular Kokoro TTS wrapper

Cleaned old scripts (brain.py, old memory scripts removed)

Stable import paths & dependency cleanup

🧠 Pipeline & Model Routing

New central Pipeline orchestrator

Router selects best model automatically

Unified generate_reply() and generate_stream() through model wrappers

🧬 Persona Engine Upgrade

Moved to core/sara_persona.py

Supports modes: gremlin, teaching, professional

Supports toggles: child mode, formal tone, emoji toggle

Supports sliders: swear level, verbosity, roast level, spontaneity

Centralized persona post-filters

🧠 Memory Engine Rewrite

Introduced MemoryManager and memory_utils

Cleaner memory formatting + relevance ranking

Proper prompt injection

🎙️ TTS Integration

Kokoro TTS modularized + safe loading

Audio output unified through pipeline

Static audio caching under /audio

🖥️ Frontend Compatibility

No UI changes required

Frontend automatically works with v1.5 backend

Ready for future cloud API adjustments

[v1.0] — 2025-12-10
Initial Release

A fully working local AI assistant featuring:

Local LLM (Ollama + Gemma3 1B)

Persona system (basic)

SQLite memory

Kokoro TTS integration

React/Vite chat UI

Memory viewer, persona panel, notes panel

Basic modular backend

Future Roadmap (from official project roadmap)
[v2.0] — Cloud Version

Deploy backend to cloud

Add authentication, environment configs

Route TTS + LLM through cloud pipelines

Optimize API stability & CORS

Prepare portfolio-ready demo instance

[v2.5] — Advanced Features

Web scraping module

Editing module (backend jobs/pods)

Tool pipeline integration

Expand memory formatting

[v3.0] — Stress Testing

Load tests

Memory leak tests

Profiling (CPU/GPU/RAM)

Latency benchmarking

Failover behavior

[v3.5] — PNG Avatar UI

PNG-based character

Emotion-based expression engine

UI redesign for avatar + chat layout

[v4.0] — Live2D Integration

Rigged model

Lip-sync with TTS

Expression blending
