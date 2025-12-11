# backend/core/pipeline.py

from typing import Any


class Pipeline:
    def __init__(self, config: Any = None):
        self.config = config

        self._persona = None
        self._memory = None
        self._tts = None

    # ---------------------------------------------------
    # MODEL LOADERS
    # ---------------------------------------------------

    def _load_casual_model(self):
        if hasattr(self, "_casual_model_loaded"):
            return
        try:
            from backend.models.local_casual import LocalCasualModel
            self.casual_model = LocalCasualModel(self.config)
        except Exception as e:
            print("Failed to load casual model:", e)
            self.casual_model = None
        self._casual_model_loaded = True

    def _load_coding_model(self):
        if hasattr(self, "_coding_model_loaded"):
            return
        try:
            from backend.models.local_coding import LocalCodingModel
            self.coding_model = LocalCodingModel(self.config)
        except Exception as e:
            print("Failed to load coding model:", e)
            self.coding_model = None
        self._coding_model_loaded = True

    def _load_teaching_model(self):
        if hasattr(self, "_teaching_model_loaded"):
            return
        try:
            from backend.models.local_teaching import LocalTeachingModel
            self.teaching_model = LocalTeachingModel(self.config)
        except Exception as e:
            print("Failed to load teaching model:", e)
            self.teaching_model = None
        self._teaching_model_loaded = True

    def _load_fast_model(self):
        if hasattr(self, "_fast_model_loaded"):
            return
        try:
            from backend.models.fast_talking import FastTalkingModel
            self.fast_model = FastTalkingModel(self.config)
        except Exception as e:
            print("Failed to load fast-talking model:", e)
            self.fast_model = None
        self._fast_model_loaded = True

    # ---------------------------------------------------
    # OPTIONAL LAZY LOADERS
    # ---------------------------------------------------
    def _load_persona(self):
        if self._persona is None:
            try:
                from backend.core.sara_persona import PersonaManager
                self._persona = PersonaManager()
            except Exception:
                self._persona = None

    def _load_memory(self):
        if self._memory is None:
            try:
                from backend.memory.memory_core import MemoryManager
                self._memory = MemoryManager(self.config)
            except Exception:
                self._memory = None

    # ---------------------------------------------------
    # MESSAGE HANDLER (NON-STREAM)
    # ---------------------------------------------------
    def handle_message(self, message: str, user_id: str = "default"):

        try:
            from backend.core.sara_router import route_to_model
            model_key = route_to_model(message)
        except Exception:
            model_key = "local_casual"

        if model_key == "local_coding":
            self._load_coding_model()
            model = self.coding_model
        elif model_key == "local_teaching":
            self._load_teaching_model()
            model = self.teaching_model
        elif model_key == "fast_talking":
            self._load_fast_model()
            model = self.fast_model
        else:
            self._load_casual_model()
            model = self.casual_model

        if not model:
            return {
                "reply": "[ERROR] Model load failed.",
                "model_used": model_key,
                "memory_update": False,
            }

        reply, memflag = model.generate_reply(message)

        return {
            "reply": reply,
            "model_used": model_key,
            "memory_update": memflag,
        }

    # ---------------------------------------------------
    # STREAMING HANDLER
    # ---------------------------------------------------
    def handle_stream(self, message: str, user_id: str = "default"):

        try:
            from backend.core.sara_router import route_to_model
            model_key = route_to_model(message)
        except Exception:
            model_key = "local_casual"

        if model_key == "local_coding":
            self._load_coding_model()
            model = self.coding_model
        elif model_key == "local_teaching":
            self._load_teaching_model()
            model = self.teaching_model
        elif model_key == "fast_talking":
            self._load_fast_model()
            model = self.fast_model
        else:
            self._load_casual_model()
            model = self.casual_model

        if not model:
            return iter([]), False

        return model.generate_stream(message)
