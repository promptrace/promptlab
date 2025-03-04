from promptrace.enums import EvalLibrary, RagasMetric
from promptrace.evaluator.evaluator import Evaluator
from promptrace.evaluator.ragas import RagasRougeScore, RagasSemanticSimilarity
from promptrace.types import ModelConfig

class EvaluatorFactory:
    
    @staticmethod
    def get_evaluator(eval_library: str, metric:str, model:ModelConfig) -> Evaluator:
        
        if eval_library == EvalLibrary.RAGAS.value:
            if metric == RagasMetric.SemanticSimilarity.value:
                return RagasSemanticSimilarity(model=model)
            if metric == RagasMetric.RougeScore.value:
                return RagasRougeScore(model=model)   
        else:
            raise ValueError(f"Unknown evaluation strategy: {eval_library}")