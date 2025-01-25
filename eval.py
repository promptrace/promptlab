from abc import ABC, abstractmethod

class Evaluation(ABC):
    @abstractmethod
    def evaluate(self, data):
        pass

class RougeLEvaluation(Evaluation):
    def evaluate(self, data):
        # Implement RougeL evaluation logic here
        return f"222"

class EvaluationFactory:
    @staticmethod
    def get_evaluation_strategy(strategy: str) -> Evaluation:
        if strategy == 'rougeL':
            return RougeLEvaluation()
        else:
            raise ValueError(f"Unknown evaluation strategy: {strategy}")