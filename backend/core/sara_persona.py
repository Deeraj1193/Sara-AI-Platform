# backend/core/sara_persona.py

import re

class PersonaManager:
    """
    Handles:
    - persona instruction generation
    - language style (professional, gremlin, teaching)
    - censorship rules (child mode, swear level)
    - verbosity/spontaneity modifiers
    """

    def __init__(self, persona: dict = None):
        # persona = { "mode": ..., "toggles": ..., "sliders": ... }
        self.persona = persona or {
            "mode": "gremlin",
            "toggles": {},
            "sliders": {},
        }

    # ----------------------------------------------------------
    # 1. Generate the persona instruction block (migrated cleanly)
    # ----------------------------------------------------------
    def build_persona_instruction(self) -> str:
        p = self.persona
        mode = p.get("mode", "gremlin")
        toggles = p.get("toggles", {})
        sliders = p.get("sliders", {})

        swear_level = int(sliders.get("swearLevel", 80))
        roast_level = int(sliders.get("roastLevel", 70))
        verbosity = int(sliders.get("verbosity", 50))
        spontaneity = int(sliders.get("spontaneity", 40))

        lines = []
        lines.append("SYSTEM PERSONA INSTRUCTIONS:")

        # --- core modes ---
        if mode == "gremlin":
            lines.append("- Default style: chaotic, bratty, playful, teasing.")
            lines.append(f"- Roasting intensity allowed: {roast_level}/100.")
        elif mode == "teaching":
            lines.append("- Default style: friendly teacher.")
            lines.append("- Prioritize clarity, guide the user step-by-step.")
            lines.append("- Avoid swearing or insulting language.")
        elif mode == "professional":
            lines.append("- Default style: concise, technical, respectful.")
            lines.append("- No swearing or teasing. Keep tone formal.")

        # --- child mode ---
        if toggles.get("childMode", False):
            lines.append("- Child mode ON: absolutely no profanity.")
        else:
            lines.append(f"- Swear preference allowed up to: {swear_level}/100.")

        # --- emoji/formal toggles ---
        if not toggles.get("useEmojis", True):
            lines.append("- Avoid emojis.")
        if toggles.get("formalTone", False):
            lines.append("- Prefer formal wording, avoid slang.")

        # --- verbosity/spontaneity ---
        lines.append(f"- Verbosity target: {verbosity}/100.")
        lines.append(f"- Spontaneity: {spontaneity}/100.")

        # --- code handling rule ---
        lines.append("- Use triple-backticks for code outputs.")

        # --- outro ---
        if mode != "professional" and not toggles.get("formalTone", False):
            lines.append("- You may add a short playful tease at the end.")

        return "\n".join(lines)

    # ----------------------------------------------------------
    # 2. Post-processing filters for model replies
    # ----------------------------------------------------------
    def apply_post_filters(self, reply: str) -> str:
        p = self.persona
        toggles = p.get("toggles", {})
        sliders = p.get("sliders", {})
        mode = p.get("mode", "gremlin")

        # child mode = full strict
        if toggles.get("childMode", False):
            return self._child_strict(reply)

        # otherwise: swear filtering according to slider
        swear_lvl = int(sliders.get("swearLevel", 80))
        reply = self._light_censor(reply, swear_lvl)

        # formal tone cleanup
        if toggles.get("formalTone", False):
            reply = self._formal_cleanup(reply)

        # professional mode removes emojis
        if mode == "professional":
            reply = self._remove_emojis(reply)

        return reply

    # ----------------------------------------------------------
    # Helper functions (cleaned versions of your brain.py logic)
    # ----------------------------------------------------------
    def _child_strict(self, text: str) -> str:
        """Full mask for all swear words."""
        return re.sub(r"[A-Za-z]", "*", text)

    def _light_censor(self, text: str, level: int) -> str:
        """Partial masking depending on swear level."""
        bad_words = ["damn", "shit", "fuck", "bitch", "asshole", "bastard", "crap", "hell"]
        for w in bad_words:
            if level < 80:
                pattern = re.compile(w, flags=re.IGNORECASE)
                text = pattern.sub(w[0] + "*" * (len(w) - 1), text)
        return text

    def _formal_cleanup(self, text: str) -> str:
        """Small slang cleanup."""
        text = re.sub(r"\b(u|ur)\b", "your", text, flags=re.IGNORECASE)
        text = text.replace(" tho", " though")
        return text

    def _remove_emojis(self, text: str) -> str:
        """Remove emojis."""
        return re.sub(r"[\U0001F300-\U0001FAD6\U0001F600-\U0001F64F]", "", text)
