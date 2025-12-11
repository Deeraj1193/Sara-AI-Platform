# backend/models/fast_talking.py

from backend.models.base_model import BaseModel


class FastTalkingModel(BaseModel):
    """
    Light-weight model used for Talking Mode (low latency).
    """

    def __init__(self, config=None):
        super().__init__(config)

    def call(self, prompt: str) -> str:
        # Minimal reply for fast talking mode.
        return "ok"

    def generate_reply(self, user_input: str):
        # Fast path: return very short reply and no memory update
        reply = self.call(user_input)
        return reply, False

    def generate_stream(self, user_input: str):
        # Streaming: yield the short reply token-by-token (here whole reply)
        def gen():
            # If you later have real token streaming, replace this generator
            yield self.call(user_input)
        return gen(), False
