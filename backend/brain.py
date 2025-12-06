# brain.py
from __future__ import annotations
from pathlib import Path
import re
import json
import requests
from typing import Tuple, List, Dict

from .persona_store import get_persona
from ..scripts.memory import init_memory, save_memory, search_memory, get_all_memories

ROOT = Path(__file__).resolve().parents[1]
init_memory()

# Load base system prompt + few-shot
system_prompt = (ROOT / "system_prompt.txt").read_text(encoding="utf-8")
fewshot_content = (ROOT / "few_shot_examples.txt").read_text(encoding="utf-8")

# Minimal swear word list (expand as you like)
_SWEARS = {
    "damn", "shit", "fuck", "bitch", "asshole", "bastard", "crap", "hell"
}


def _sanitize_text_for_child(text: str) -> str:
    """Replace any swear words with **** (child mode strict)."""
    def repl(m):
        w = m.group(0)
        return "*" * len(w)
    pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in _SWEARS) + r")\b", flags=re.IGNORECASE)
    return pattern.sub(repl, text)


def _light_censor(text: str, swear_level: int) -> str:
    """
    Simple rule: if swear_level < 50 mask common swear words,
    if >= 50 allow partial, if >=80 allow fully.
    """
    if swear_level >= 80:
        return text  # allow
    if swear_level >= 50:
        # mask part of word (keep first letter)
        def repl(m):
            w = m.group(0)
            if len(w) <= 2:
                return "*" * len(w)
            return w[0] + "*" * (len(w) - 1)
        pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in _SWEARS) + r")\b", flags=re.IGNORECASE)
        return pattern.sub(repl, text)
    # low level: full mask
    return _sanitize_text_for_child(text)


def _persona_instructions(persona: Dict) -> str:
    """
    Convert persona object into a crisp system instruction block appended
    to the base system prompt.
    """
    mode = persona.get("mode", "gremlin")
    toggles = persona.get("toggles", {})
    sliders = persona.get("sliders", {})

    swear_level = int(sliders.get("swearLevel", 80))
    roast_level = int(sliders.get("roastLevel", 70))
    verbosity = int(sliders.get("verbosity", 50))
    spontaneity = int(sliders.get("spontaneity", 40))

    lines = []
    lines.append("SYSTEM PERSONA INSTRUCTIONS:")
    # Core: mode-specific guidance
    if mode == "gremlin":
        lines.append("- Default style: chaotic, bratty, teasing, tsundere sometimes.")
        lines.append("- Tone: playful, snarky, full gremlin energy.")
        lines.append(f"- Allowed to roast user. Roasting intensity: {roast_level}/100.")
    elif mode == "teaching":
        lines.append("- Default style: friendly teacher. Prioritize clarity and understanding.")
        lines.append("- Avoid swearing. Use examples and step-by-step explanations.")
        lines.append("- Ask questions to ensure the user understands.")
    elif mode == "professional":
        lines.append("- Default style: professional, concise, technical.")
        lines.append("- Do not use swearing or insults. Provide clean code blocks when requested.")
        lines.append("- Focus on correctness and readability of answers.")

    # Swear and child rules
    if toggles.get("childMode", False):
        lines.append("- Child mode ON: do NOT use profanity. Replace or avoid explicit curse words.")
    else:
        lines.append(f"- Swear preference: allowed level {swear_level}/100 (higher = more permissive).")

    # Emojis and formal tone
    if not toggles.get("useEmojis", True):
        lines.append("- Avoid using emojis in replies.")
    if toggles.get("formalTone", False):
        lines.append("- Prefer formal wording and avoid casual slang.")

    # Verbosity & spontaneity hints
    lines.append(f"- Verbosity target: {verbosity}/100 (lower = concise, higher = more detail).")
    lines.append(f"- Spontaneity preference: {spontaneity}/100 (higher = more unexpected jokes).")

    # Code output rule (ensure code blocks are used)
    lines.append("- When producing code: always use triple-backtick fenced blocks and preserve indentation.")
    lines.append("- When giving multi-step instructions, number steps and be concise unless verbosity high.")

    # Sign-off: prefer to keep playful teaser at end (unless professional)
    if mode != "professional" and not toggles.get("formalTone", False):
        lines.append("- Optionally include a short playful tease at the END of the message (keep it brief).")

    return "\n".join(lines)


def format_memory_hybrid(raw_text: str) -> str:
    text = raw_text.strip().rstrip(".").strip()
    lower = text.lower()
    m = re.match(r"my\s+([\w\s'-]+?)\s+(?:name\s+is|is)\s+(.+)", lower)
    if m:
        subject = m.group(1).strip()
        value = m.group(2).strip()
        key = subject.replace(" ", "_")
        val_display = value.capitalize()
        return (
            f"- The user's {subject} is {val_display}.    "
            f"[type: relation, key: {key}, value: {val_display}]"
        )
    m = re.match(r"(?:i\s+(?:like|love|enjoy|prefer))\s+(.+)", lower)
    if m:
        val = m.group(1).strip()
        return (
            f"- The user likes {val}.    "
            f"[type: preference, key: likes, value: {val}]"
        )
    m = re.match(r"(?:i am|i'm)\s+(.+)", lower)
    if m:
        val = m.group(1).strip().capitalize()
        return (
            f"- The user's identity description: {val}.    "
            f"[type: identity, key: desc, value: {val}]"
        )
    m = re.match(r"([\w\s'-]+)\s+is\s+(.+)", text)
    if m:
        ent = m.group(1).strip()
        action = m.group(2).strip()
        ent_clean = ent.capitalize()
        return (
            f"- {ent_clean} (the user's referenced entity) is {action}.    "
            f"[type: action, key: {ent_clean.lower()}_action, value: {action}]"
        )
    safe = text.replace("\n", " ").strip()
    return (
        f"- The user said: \"{safe}\".    "
        f"[type: fact, key: misc, value: {safe}]"
    )


def query_ollama_raw(messages: List[dict], stream: bool = False) -> dict:
    """
    Call the Ollama HTTP endpoint. Returns the response object (requests.Response).
    stream=False returns JSON; stream=True returns the Response for streaming iteration.
    """
    payload = {
        "model": "gemma3:1b",
        "messages": messages,
        "stream": stream
    }
    url = "http://localhost:11434/api/chat"
    if stream:
        return requests.post(url, json=payload, stream=True)
    else:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()


def build_prompt(user_input: str) -> Tuple[List[dict], bool]:
    """
    Build the message list for the model. Inject persona overrides per-request.
    """
    persona = get_persona()

    persona_instr = _persona_instructions(persona)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": persona_instr},
        {"role": "system", "content": "FEW SHOT EXAMPLES:\n" + fewshot_content},
    ]

    relevant = search_memory(user_input)
    if relevant:
        messages.append({
            "role": "system",
            "content": "USER MEMORY FACTS:\n" + "\n".join(relevant) + "\nUse these facts when answering."
        })

    messages.append({"role": "user", "content": user_input})

    # detect memory save
    lower = user_input.lower()
    save_flag = (not user_input.endswith("?") and any(k in lower for k in [" i ", " my ", " im ", " i'm ", " me "]))
    if save_flag:
        try:
            save_memory(format_memory_hybrid(user_input))
        except Exception:
            pass

    return messages, save_flag


def generate_reply(user_input: str) -> Tuple[str, bool]:
    """
    Primary non-streaming reply path used by frontend:
    - builds a prompt augmented with persona instructions,
    - calls Ollama,
    - applies post-processing (child mode / swear-level)
    """
    persona = get_persona()
    messages, memflag = build_prompt(user_input)

    try:
        data = query_ollama_raw(messages, stream=False)
        # Ollama response shape: { "message": {"role": "assistant","content": "..."} , ...}
        reply = data.get("message", {}).get("content", "[No reply]")
    except Exception as e:
        reply = f"[ERROR] Model call failed: {e}"
        return reply, memflag

    # Post-process according to persona
    # Child mode: strict clean
    if persona.get("toggles", {}).get("childMode", False):
        reply = _sanitize_text_for_child(reply)
    else:
        # apply lighter censorship according to swear level
        swear_lvl = int(persona.get("sliders", {}).get("swearLevel", 80))
        reply = _light_censor(reply, swear_lvl)

    # If formal tone requested, do a light normalization (very simple)
    if persona.get("toggles", {}).get("formalTone", False):
        # A lightweight pass to remove some slang patterns; keep it simple.
        reply = re.sub(r"\b(u|ur)\b", "your", reply, flags=re.IGNORECASE)
        reply = reply.replace("tho", "though")

    # If professional mode requested, ensure no playful tags or emoji (best-effort)
    if persona.get("mode", "") == "professional":
        # remove simple emoji characters
        reply = re.sub(r"[\U0001F300-\U0001FAD6\U0001F600-\U0001F64F]", "", reply)
        # remove emotion tags like [emotion: ...]
        reply = re.sub(r"\[.*?emotion.*?\]", "", reply, flags=re.IGNORECASE)

    return reply, memflag


# Streaming path (keeps same behavior but sanitizes tokens lightly)
def stream_model_reply(messages: List[dict]):
    """
    Stream tokens from Ollama and yield sanitized chunks.
    """
    r = query_ollama_raw(messages, stream=True)
    r.raise_for_status()
    persona = get_persona()
    swear_lvl = int(persona.get("sliders", {}).get("swearLevel", 80))
    child = persona.get("toggles", {}).get("childMode", False)

    for line in r.iter_lines():
        if not line:
            continue
        try:
            obj = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError:
            continue

        if "message" in obj and "content" in obj["message"]:
            chunk = obj["message"]["content"]
            if child:
                chunk = _sanitize_text_for_child(chunk)
            else:
                chunk = _light_censor(chunk, swear_lvl)

            yield chunk

        if obj.get("done", False):
            break


def generate_stream(user_input: str):
    messages, memflag = build_prompt(user_input)
    return stream_model_reply(messages), memflag


def list_all_memories():
    return list(get_all_memories())
