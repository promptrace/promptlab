from abc import ABC, abstractmethod

from promptrace.config import ModelConfig
from promptrace.types import InferenceResult

class Model(ABC):
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config

    @abstractmethod
    def invoke(self, system_prompt: str, user_prompt: str)->InferenceResult:
        pass