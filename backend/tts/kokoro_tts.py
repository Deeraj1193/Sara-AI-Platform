# backend/tts/kokoro_tts.py

import base64
import io
import numpy as np
import soundfile as sf
from kokoro import KPipeline


class KokoroTTS:
    def __init__(self, voice="af_heart"):
        self.pipeline = None
        self.voice = voice  # Default female voice

    def load(self):
        if self.pipeline is None:
            print(f"[KokoroTTS] Loading Kokoro model (voice = {self.voice})...")
            self.pipeline = KPipeline("a")  # American English
            print("[KokoroTTS] Model loaded.")

    def synthesize(self, text: str, speed: float = 1.0) -> bytes:
        self.load()

        gen = self.pipeline(text, voice=self.voice, speed=speed)

        audio_chunks = []

        for chunk in gen:
            # expected: (text, ipa, audio_tensor)
            if len(chunk) != 3:
                continue

            audio = chunk[2]

            # convert torch -> numpy
            if hasattr(audio, "detach"):
                audio = audio.detach().cpu().numpy()

            # ensure float32
            audio = np.asarray(audio, dtype="float32")

            # sanity filter
            if audio.ndim != 1:
                continue
            if audio.size == 0:
                continue

            # add chunk
            audio_chunks.append(audio)

        if not audio_chunks:
            raise RuntimeError("Kokoro returned no valid audio tensors.")

        # concatenate final waveform
        audio = np.concatenate(audio_chunks, axis=0)

        # write WAV to memory
        buf = io.BytesIO()
        sf.write(buf, audio, 24000, format="WAV")
        return buf.getvalue()

    def synthesize_base64(self, text: str, speed: float = 1.0) -> str:
        wav = self.synthesize(text, speed)
        return base64.b64encode(wav).decode("utf-8")


kokoro = KokoroTTS()
