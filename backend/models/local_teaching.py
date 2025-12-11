# backend/models/local_teaching.py

from backend.models.base_model import BaseModel


class LocalTeachingModel(BaseModel):
    """
    Model wrapper for teaching/explanation style replies.
    """

    def __init__(self, config=None):
        super().__init__(config)

    def call(self, prompt: str) -> str:
        # TODO: replace with real prompt + call logic
        return "placeholder teaching reply"
