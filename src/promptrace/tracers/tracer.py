from abc import ABC, abstractmethod
from promptrace.config import EvaluationConfig

class Tracer(ABC):
    def __init__(self, trace_target):
        self.trace_target = trace_target

    @abstractmethod
    def trace(self, result, evaluations: list[EvaluationConfig]):
        pass