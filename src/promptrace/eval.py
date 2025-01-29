from abc import ABC, abstractmethod
from promptrace.parser import Prompt

class Evaluation(ABC):
    @abstractmethod
    def evaluate(self, data):
        pass

class IsNumericEvaluator(Evaluation):
    def evaluate(self, data: Prompt):
        val = False
        if isinstance(data.inference, (int, float)):
            val = True
        elif isinstance(data.inference, str):
            try:
                float(data.inference)
                val = True
            except ValueError:
                pass
        data.evaluation_result = {'is_numeric': val}

class EvaluationFactory:
    @staticmethod
    def get_evaluator(strategy: str) -> Evaluation:
        if strategy == 'is_numeric':
            return IsNumericEvaluator()
        else:
            raise ValueError(f"Unknown evaluation strategy: {strategy}")