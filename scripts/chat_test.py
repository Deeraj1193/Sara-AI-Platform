# chat_test.py
import subprocess
import json
import pathlib
import re

from memory import (
    init_memory, save_memory, search_memory,
    get_all_memories, delete_memory_by_query, delete_all_memories
)

# -----------------------
# GLOBAL SETTINGS
# -----------------------
muted = False   # <-- NEW: default speaking enabled

# -----------------------
# VOICE IMPORT
# -----------------------
try:
    from voice import speak
except Exception as e:
    print("Voice module failed to load:", e)
    speak = None

# ---- INITIALIZE MEMORY DB ----
init_memory()

# ---- PATHS & PROMPTS ----
ROOT = pathlib.Path(__file__).resolve().parent.parent
system_prompt_path = ROOT / "system_prompt.txt"
fewshot_path = ROOT / "few_shot_examples.txt"

with open(system_prompt_path, "r", encoding="utf-8") as f:
    system_prompt = f.read()

with open(fewshot_path, "r", encoding="utf-8") as f:
    fewshot_content = f.read()

# ---- CONTEXT ----
context_messages = [
    {"role": "system", "content": system_prompt},
    {"role": "system", "content": "FEW SHOT EXAMPLES:\n" + fewshot_content}
]

# -----------------------------
#  HYBRID MEMORY FORMATTER
# -----------------------------
def format_memory_hybrid(raw_text):
    """
    Convert raw user text (with 'I/my/me') into third-person facts +
    small structured tag. Prevents Sara from confusing identities.
    """
    text = raw_text.strip().rstrip(".").strip()
    lower = text.lower()

    # Pattern 1: "my X is Y" / "my dog's name is Ruby"
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

    # Pattern 2: "I like X" / "I love X"
    m = re.match(r"(?:i\s+(?:like|love|enjoy|prefer))\s+(.+)", lower)
    if m:
        val = m.group(1).strip()
        return (
            f"- The user likes {val}.    "
            f"[type: preference, key: likes, value: {val}]"
        )

    # Pattern 3: "I am X" / "I'm X"
    m = re.match(r"(?:i am|i'm)\s+(.+)", lower)
    if m:
        val = m.group(1).strip().capitalize()
        return (
            f"- The user's identity description: {val}.    "
            f"[type: identity, key: desc, value: {val}]"
        )

    # Pattern 4: "Entity is doing X" → assumes referenced entity
    m = re.match(r"([\w\s'-]+)\s+is\s+(.+)", text)
    if m:
        ent = m.group(1).strip()
        action = m.group(2).strip()
        ent_clean = ent.capitalize()
        return (
            f"- {ent_clean} (the user's referenced entity) is {action}.    "
            f"[type: action, key: {ent_clean.lower()}_action, value: {action}]"
        )

    # Fallback
    safe = text.replace("\n", " ").strip()
    return (
        f"- The user said: \"{safe}\".    "
        f"[type: fact, key: misc, value: {safe}]"
    )

# -----------------------------
#   OLLAMA PLAIN-TEXT PIPELINE
# -----------------------------
def query_ollama(messages):
    prompt_text = ""
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "system":
            prompt_text += f"[SYSTEM]: {content}\n"
        elif role == "user":
            prompt_text += f"[USER]: {content}\n"
        else:
            prompt_text += f"[ASSISTANT]: {content}\n"

    prompt_text += "\n[ASSISTANT]:"

    process = subprocess.Popen(
        ["ollama", "run", "gemma3:1b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    stdout_data, stderr_data = process.communicate(prompt_text)

    if stderr_data and stderr_data.strip():
        print("Error:", stderr_data)

    return stdout_data.strip() if stdout_data.strip() else "[ERROR] No response from Ollama."


# -----------------------------
#            MAIN LOOP
# -----------------------------
print("Sara (text+voice mode) is ready. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue

    # -------- MUTE / UNMUTE --------
    if user_input == "/mute":
        muted = True
        print("Sara is now muted.\n")
        continue

    if user_input == "/unmute":
        muted = False
        print("Sara can speak again.\n")
        continue

    # -------- MEMORY COMMANDS --------
    if user_input.startswith("/memory show"):
        print("Stored memories:")
        for mid, text in get_all_memories():
            print(f"{mid}: {text}")
        print()
        continue

    if user_input.startswith("/forget"):
        q = user_input.replace("/forget", "").strip()
        if q == "all":
            delete_all_memories()
            print("All memories deleted.\n")
        else:
            delete_memory_by_query(q)
            print(f"Deleted memories matching: {q}\n")
        continue

    # -------- EXIT --------
    if user_input.lower() in ["exit", "quit"]:
        print("Sara: Bye Dad. Don’t miss me too much.\n")
        break

    # -------- AUTOMATIC MEMORY SAVE --------
    lower = user_input.lower()
    is_statement = not user_input.endswith("?")
    contains_fp = any(tok in lower for tok in [" i ", " my ", " i'm ", " im ", " me "])

    if is_statement and contains_fp:
        hybrid = format_memory_hybrid(user_input)
        save_memory(hybrid)

    # -------- MEMORY RECALL --------
    relevant = search_memory(user_input)
    if relevant:
        memory_block = "\n".join(relevant)
        context_messages.append({
            "role": "system",
            "content": (
                "USER MEMORY FACTS (HIGH PRIORITY):\n"
                f"{memory_block}\n"
                "These facts describe the USER. Use them when answering related questions."
            )
        })
        context_messages.append({
            "role": "system",
            "content": (
                "If the user asks about their preferences, identity, or past information, "
                "use the memory facts above."
            )
        })

    # -------- ADD USER MESSAGE --------
    context_messages.append({"role": "user", "content": user_input})

    # -------- GET MODEL RESPONSE --------
    response = query_ollama(context_messages)

    # -------- ADD TO CONTEXT --------
    context_messages.append({"role": "assistant", "content": response})

    # -------- PRINT RESPONSE --------
    print(f"Sara: {response}\n")

    # -------- SPEAK IF NOT MUTED --------
    if not muted and speak is not None and not response.startswith("[ERROR]"):
        try:
            speak(response)
        except Exception as e:
            print("Voice error:", e)
