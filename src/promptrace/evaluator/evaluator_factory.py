from promptrace.enums import EvaluationMetric
from promptrace.evaluator.evaluator import Evaluator
from promptrace.evaluator.is_numeric import IsNumericEvaluator
from promptrace.evaluator.length import LengthEvaluator


class EvaluatorFactory:
    @staticmethod
    def get_evaluator(strategy: str) -> Evaluator:
        if strategy == EvaluationMetric.IS_NUMERIC.value:
            return IsNumericEvaluator()
        if strategy == EvaluationMetric.LENGTH.value:
            return LengthEvaluator()
        else:
            raise ValueError(f"Unknown evaluation strategy: {strategy}")