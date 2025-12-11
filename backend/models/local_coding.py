# backend/models/local_coding.py

from backend.models.base_model import BaseModel


class LocalCodingModel(BaseModel):
    """
    Model wrapper for coding/debug/technical queries.
    Structure mirrors LocalCasualModel's API.
    """

    def __init__(self, config=None):
        super().__init__(config)

    def call(self, prompt: str) -> str:
        # TODO: replace with actual model call / prompt builder
        return "placeholder coding reply"

    # Optional: inherit generate_reply / generate_stream from BaseModel
