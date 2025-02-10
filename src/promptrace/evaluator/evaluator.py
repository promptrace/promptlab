from abc import ABC, abstractmethod

 
class Evaluator(ABC):
    
    @abstractmethod
    def evaluate(self, inference: str, expected_value: str):
        pass