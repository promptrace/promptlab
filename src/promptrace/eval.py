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

class EvaluationFactory:
    @staticmethod
    def get_evaluator(strategy: str) -> Evaluation:
        if strategy == EvaluationMetric.IS_NUMERIC.value:
            return IsNumericEvaluator()
        else:
            raise ValueError(f"Unknown evaluation strategy: {strategy}")