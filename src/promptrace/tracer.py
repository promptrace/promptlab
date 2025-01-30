import os
from datetime import datetime
from abc import ABC, abstractmethod
import uuid
from promptrace.config import EvaluationConfig, ModelConfig
from promptrace.enums import TracerType
import csv

class Tracer(ABC):
    def __init__(self, trace_target):
        self.trace_target = trace_target

    @abstractmethod
    def trace(self, experiment, evaluations: list[EvaluationConfig]):
        pass

class FileTracer(Tracer):
    def trace(self, experiment, evaluations: list[EvaluationConfig]):
        file_name = datetime.now().strftime("run.%Y%m%d.%H%M%S.txt")
        file_path = os.path.join(self.trace_target, file_name)

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')

            headers = ['exp_id','model_type','model','prompt_template', 'user_prompt','system_prompt', 'dataset', 'inference', 'prompt_token', 'completion_token'] + [evaluation.metric for evaluation in evaluations]
            writer.writerow(headers)
            experiment_id = str(uuid.uuid4())

            for item in experiment:
                item.insert(0, experiment_id)
                writer.writerow(item)

class TracerFactory:
    @staticmethod
    def get_tracer(tracer_type: str, trace_target:str) -> Tracer:
        if tracer_type == TracerType.FILE.value:
            return FileTracer(trace_target)
        else:
            raise ValueError(f"Unknown tracer: {tracer_type}")