from abc import ABC, abstractmethod
from promptrace.enums import EvaluationMetric

class Evaluation(ABC):
    @abstractmethod
    def evaluate(self, data):
        pass

class IsNumericEvaluator(Evaluation):
    def evaluate(self, data: str):
        val = False
        if isinstance(data, (int, float)):
            val = True
        elif isinstance(data, str):
            try:
                float(data)
                val = True
            except ValueError:
                pass
        
        return val
    
class LengthEvaluator(Evaluation):
    def evaluate(self, data: str):
       
        return len(str(data))

class EvaluationFactory:
    @staticmethod
    def get_evaluator(strategy: str) -> Evaluation:
        if strategy == EvaluationMetric.IS_NUMERIC.value:
            return IsNumericEvaluator()
        if strategy == EvaluationMetric.LENGTH.value:
            return LengthEvaluator()
        else:
            raise ValueError(f"Unknown evaluation strategy: {strategy}")