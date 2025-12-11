# backend/models/local_casual.py

import requests
import json
import re
from pathlib import Path

from backend.models.base_model import BaseModel
from backend.core.sara_persona import PersonaManager
from backend.memory.memory_utils import should_store_memory
from backend.memory.memory_core import MemoryManager


class LocalCasualModel(BaseModel):
    """
    Wrapper for the casual chat model (Ollama).
    This class will eventually integrate with the full pipeline.
    """

    def __init__(self, config=None):
        super().__init__(config)

        # Lazy persona loader (loads persona store later)
        try:
            from backend.persona_store import get_persona
            self.persona_data = get_persona()
        except Exception:
            self.persona_data = {"mode": "gremlin", "toggles": {}, "sliders": {}}

        self.persona_manager = PersonaManager(self.persona_data)

    # ------------------------------------------------
    # 1. RAW OLLAMA CALL
    # ------------------------------------------------
    def _query_ollama_raw(self, messages, stream=False):
        payload = {
            "model": "gemma3:1b",
            "messages": messages,
            "stream": stream,
        }
        url = "http://localhost:11434/api/chat"

        if stream:
            return requests.post(url, json=payload, stream=True)
        else:
            r = requests.post(url, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()

    # ------------------------------------------------
    # 2. call() placeholder (will be replaced later)
    # ------------------------------------------------
    def call(self, prompt):
        return "placeholder casual reply"

    # ------------------------------------------------
    # 3. Build Prompt (from brain.py, corrected)
    # ------------------------------------------------
    def _build_prompt(self, user_input: str):
        # Persona load
        try:
            from backend.persona_store import get_persona
            persona = get_persona()
        except Exception:
            persona = {"mode": "gremlin", "toggles": {}, "sliders": {}}

        # Load system prompt files from project root
        try:
            proj_root = Path(__file__).resolve().parents[2]
            system_prompt = (proj_root / "system_prompt.txt").read_text(encoding="utf-8")
            fewshot_content = (proj_root / "few_shot_examples.txt").read_text(encoding="utf-8")
        except Exception:
            system_prompt = "SYSTEM PROMPT MISSING"
            fewshot_content = ""

        # Persona instructions
        try:
            persona_instr = self.persona_manager.build_persona_instruction()
        except Exception:
            persona_instr = f"Persona mode: {persona.get('mode', 'gremlin')}"

        # Build messages list
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": persona_instr},
            {"role": "system", "content": "FEW SHOT EXAMPLES:\n" + fewshot_content},
        ]

        # Memory injection
        try:
            mem = MemoryManager(self.config)
            relevant = mem.query("default", user_input, top_k=3)
        except Exception:
            relevant = []

        if relevant:
            messages.append({
                "role": "system",
                "content": "USER MEMORY FACTS:\n" + "\n".join(relevant)
            })

        # Add user message
        messages.append({"role": "user", "content": user_input})

        # Memory save detection
        memflag = should_store_memory(user_input)

        return messages, memflag

    # ------------------------------------------------
    # 4. generate_reply() — main non-streaming reply
    # ------------------------------------------------
    def generate_reply(self, user_input: str):
        messages, memflag = self._build_prompt(user_input)

        # LLM call
        try:
            data = self._query_ollama_raw(messages, stream=False)
            reply = data.get("message", {}).get("content", "[No reply]")
        except Exception as e:
            return f"[ERROR] Model call failed: {e}", memflag

        # Persona filters
        reply = self.persona_manager.apply_post_filters(reply)

        return reply, memflag

    # ------------------------------------------------
    # 5. Streaming support
    # ------------------------------------------------
    def _stream_model_reply(self, messages):
        resp = self._query_ollama_raw(messages, stream=True)
        resp.raise_for_status()

        # Load persona again for filters
        try:
            from backend.persona_store import get_persona
            persona = get_persona()
        except Exception:
            persona = {"toggles": {}, "sliders": {}, "mode": "gremlin"}

        swear_lvl = int(persona.get("sliders", {}).get("swearLevel", 80))
        child = persona.get("toggles", {}).get("childMode", False)

        for line in resp.iter_lines():
            if not line:
                continue
            try:
                obj = json.loads(line.decode("utf-8"))
            except Exception:
                continue

            if "message" in obj and "content" in obj["message"]:
                chunk = obj["message"]["content"]

                # Apply filters
                if child:
                    chunk = self.persona_manager._sanitize_full(chunk)
                else:
                    chunk = self.persona_manager._light_censor(chunk, swear_lvl)

                yield chunk

            if obj.get("done", False):
                break

    # Public pipeline streaming API
    def generate_stream(self, user_input: str):
        messages, memflag = self._build_prompt(user_input)
        return self._stream_model_reply(messages), memflag
