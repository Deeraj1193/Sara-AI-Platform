# voice.py
import torch
from torch.serialization import add_safe_globals
from playsound import playsound
import os

# --- Allow the XTTS config class load (Patch for PyTorch 2.6) ---
import TTS.tts.configs.xtts_config as xtts_cfg
add_safe_globals([xtts_cfg.XttsConfig])

# --- Import XTTS Model ---
from TTS.tts.models.xtts.xtts import Xtts
from TTS.utils.manage import ModelManager

AUDIO_OUTPUT = "sara_output.wav"

tts_model = None

try:
    # Download / load XTTS_v2 using ModelManager
    manager = ModelManager()
    model_path, config_path, _ = manager.download_model("tts_models/multilingual/multi-dataset/xtts_v2")

    # Load config
    config = xtts_cfg.XttsConfig()
    config.load_json(config_path)

    # Initialize XTTS model
    tts_model = Xtts.init_from_config(config)
    tts_model.load_checkpoint(config, model_path, use_deepspeed=False)

    print("XTTS voice model loaded successfully.")
except Exception as e:
    print("XTTS loading failed:", e)
    tts_model = None


def speak(text):
    """Generate speech and play it."""
    if tts_model is None:
        print("Voice disabled (model not loaded).")
        return

    try:
        wav = tts_model.inference(
            text=text,
            speaker="female-en-5",
            language="en",
            speed=1.05,
            emotion="happy"
        )

        # Write wav
        import soundfile as sf
        sf.write(AUDIO_OUTPUT, wav["wav"], 24000)

        playsound(AUDIO_OUTPUT)

    except Exception as e:
        print("Voice error:", e)
