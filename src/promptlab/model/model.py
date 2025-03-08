from abc import ABC, abstractmethod

from promptlab.types import InferenceResult, ModelConfig


class Model(ABC):
    
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config

    @abstractmethod
    def invoke(self, system_prompt: str, user_prompt: str)->InferenceResult:
        pass