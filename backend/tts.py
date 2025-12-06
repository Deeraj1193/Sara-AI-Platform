# tts.py
"""
Stable Coqui TTS wrapper for Sara backend.

Features:
- Singleton loader (model loads once).
- Safe-globals patching for XTTS classes commonly needed on Windows.
- Async-friendly synth using asyncio.to_thread to avoid blocking the event loop.
- Optional speaker_wav support (speaker cloning) and caching of output files.
- Returns WAV bytes (in-memory) so server can stream them to frontend.
"""

import io
import os
import tempfile
import threading
import traceback
from typing import Optional

# prefer relative imports when used as package
from pathlib import Path
import asyncio

# heavy imports only inside functions to keep module import cheap
# but we'll import torch when initializing model
MODEL_NAME = os.environ.get("SARA_TTS_MODEL", "tts_models/multilingual/xtts_v2")
# default speaker_wav path or None
DEFAULT_REF_WAV = os.environ.get("SARA_TTS_REF_WAV", None)

_lock = threading.Lock()
_instance = None


class TTSWrapper:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.tts = None
        self._loaded = False
        self._loading_exc = None

    def load(self):
        """
        Loads the model. Idempotent.
        May raise exceptions if model fails to load.
        """
        if self._loaded:
            return

        # guard so only one thread attempts load
        with _lock:
            if self._loaded:
                return
            try:
                # Import here to avoid heavy import on module import
                import torch

                # Common problematic classes for XTTS pickles;
                # add them to safe globals if available in this TTS installation.
                # If a class isn't present we ignore — this is a best-effort.
                try:
                    # try several known names that may be required
                    from TTS.tts.configs.xtts_config import XttsConfig  # type: ignore
                    torch.serialization.add_safe_globals([XttsConfig])
                except Exception:
                    pass

                try:
                    from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs  # type: ignore
                    torch.serialization.add_safe_globals([XttsAudioConfig, XttsArgs])
                except Exception:
                    pass

                try:
                    from TTS.config.shared_configs import BaseDatasetConfig  # type: ignore
                    torch.serialization.add_safe_globals([BaseDatasetConfig])
                except Exception:
                    pass

                # Now import the TTS API and initialize
                from TTS.api import TTS  # type: ignore

                # instantiate (this downloads model if needed)
                self.tts = TTS(self.model_name)
                self._loaded = True
            except Exception as e:
                self._loading_exc = e
                tb = traceback.format_exc()
                # propagate
                raise RuntimeError(f"TTS model load failed: {e}\n{tb}") from e

    async def ensure_loaded(self):
        """
        Async wrapper to load model in background thread if not loaded.
        """
        if self._loaded:
            return

        loop = asyncio.get_running_loop()
        # run blocking load in threadpool
        await loop.run_in_executor(None, self.load)

    async def synthesize_wav_bytes(
        self,
        text: str,
        speaker_wav: Optional[str] = None,
        language: Optional[str] = None,
        speaker: Optional[str] = None,
    ) -> bytes:
        """
        Synthesize the text and return WAV bytes.
        Runs blocking TTS in threadpool so FastAPI stays responsive.

        Arguments:
        - text: str - text to synthesize
        - speaker_wav: optional path to reference audio (for XTTS speaker cloning)
        - language: optional language code (e.g., "en")
        - speaker: optional speaker id (when model supports named speakers)
        """
        await self.ensure_loaded()

        def _synth():
            # Use tmp file then read back bytes (Coqui TTS writes WAV)
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".wav")
            os.close(tmp_fd)
            try:
                # tts.tts_to_file is blocking
                kwargs = {}
                if speaker_wav:
                    kwargs["speaker_wav"] = speaker_wav
                if language:
                    kwargs["language"] = language
                if speaker:
                    kwargs["speaker"] = speaker

                # Note: some models require speaker arg for multi-speaker models
                self.tts.tts_to_file(text=text, file_path=tmp_path, **kwargs)

                # read bytes
                with open(tmp_path, "rb") as fh:
                    data = fh.read()
                return data
            finally:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

        loop = asyncio.get_running_loop()
        # run TTS in a thread to avoid blocking
        wav_bytes = await loop.run_in_executor(None, _synth)
        return wav_bytes


def get_tts_singleton() -> TTSWrapper:
    global _instance
    if _instance is None:
        _instance = TTSWrapper(MODEL_NAME)
    return _instance
