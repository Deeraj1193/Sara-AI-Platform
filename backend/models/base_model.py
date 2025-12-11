# backend/models/base_model.py

from typing import Generator, Tuple, Any


class BaseModel:
    """
    Base model interface for all model wrappers.
    Subclasses should implement `call(prompt)` for non-stream responses,
    and may optionally implement `_stream_call(messages)` for streaming.
    """

    def __init__(self, config: Any = None):
        self.config = config

    # Primary synchronous call — subclasses **must** implement this.
    def call(self, prompt: str) -> str:
        raise NotImplementedError("call() must be implemented in subclasses.")

    # Public non-streaming wrapper expected by pipeline
    def generate_reply(self, user_input: str) -> Tuple[str, bool]:
        """
        Default behavior:
        - call(prompt) → returns reply string
        - second value is memory_flag (False by default)
        Subclasses may override for more complex behavior.
        """
        reply = self.call(user_input)
        return reply, False

    # Public streaming wrapper expected by pipeline
    def generate_stream(self, user_input: str) -> Tuple[Generator[str, None, None], bool]:
        """
        Default streaming wrapper which yields the full reply once.
        Subclasses that support true streaming should override.
        """
        def gen():
            yield self.call(user_input)

        return gen(), False
