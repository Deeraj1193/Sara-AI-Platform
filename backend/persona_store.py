# persona_store.py
# Global persona storage for Sara (simple in-memory store).
# Frontend reads/writes via /api/persona in server.py

from typing import Dict, Any

# Default persona config (matches your UI shape)
_DEFAULT: Dict[str, Any] = {
    "mode": "gremlin",  # gremlin | teaching | professional
    "toggles": {
        "useEmojis": True,
        "formalTone": False,
        "childMode": False,
        "soundOn": True,
        "freeTalk": False,
    },
    "sliders": {
        "swearLevel": 80,
        "roastLevel": 70,
        "verbosity": 50,
        "spontaneity": 40,
    },
}

# In-memory store (global)
_persona = _DEFAULT.copy()


def get_persona() -> Dict[str, Any]:
    # return a shallow copy to avoid accidental mutation
    return {
        "mode": _persona.get("mode", _DEFAULT["mode"]),
        "toggles": dict(_persona.get("toggles", _DEFAULT["toggles"])),
        "sliders": dict(_persona.get("sliders", _DEFAULT["sliders"])),
    }


def set_persona(new_conf: Dict[str, Any]) -> None:
    # update in place to keep references stable
    _persona.clear()
    _persona.update(new_conf)
