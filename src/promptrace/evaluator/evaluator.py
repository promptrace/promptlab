from abc import ABC, abstractmethod
from promptrace.config import ModelConfig
 
class Evaluator(ABC):
    
    def __init__(self, model: ModelConfig):
        self.model = model

    @abstractmethod
    def evaluate(self, data: dict):
        pass