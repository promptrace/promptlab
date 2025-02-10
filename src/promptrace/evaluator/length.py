from promptrace.evaluator.evaluator import Evaluator


class LengthEvaluator(Evaluator):
    def evaluate(self, inference: str, expected_value: str = None):
       
        return len(str(inference))