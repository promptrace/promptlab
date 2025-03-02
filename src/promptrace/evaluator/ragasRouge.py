from promptrace.evaluator.evaluator import Evaluator


class RagasRougeEvaluator(Evaluator):
    
    def evaluate(self, inference: str, expected_value: str = None):
       #code that usese Ragas to evaluate the inference
        return len(str(inference))