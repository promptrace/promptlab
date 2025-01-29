import os
from datetime import datetime
from abc import ABC, abstractmethod
from promptrace.parser import Experiment
from promptrace.config import ModelConfig
import csv

class Tracer(ABC):
    def __init__(self, trace_target):
        self.trace_target = trace_target

    @abstractmethod
    def trace(self, experiment: Experiment, model_params: ModelConfig):
        pass

class FileTracer(Tracer):
    def trace(self, experiment: Experiment, model_params: ModelConfig):
        file_name = datetime.now().strftime("run.%Y%m%d.%H%M%S.txt")
        file_path = os.path.join(self.trace_target, file_name)

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')

            headers = ['exp_id','model_type','model','prompt_template', 'user_prompt','system_prompt', 'dataset', 'inference', 'prompt_token', 'completion_token'] + [evaluation.metric for evaluation in experiment.evaluations]
            writer.writerow(headers)

            # Iterate over prompts
            for prompt in experiment.prompts:
                # Extract data for each prompt
                prompt_data = [experiment.experiment_id, model_params.type, model_params.deployment, experiment.prompt_template, prompt.user, prompt.system, experiment.dataset, prompt.inference, prompt.prompt_token, prompt.completion_token]
                
                # Extract evaluation results for each prompt
                if prompt.evaluation_result:
                    metrics_values = [prompt.evaluation_result.get(evaluation.metric, '') for evaluation in experiment.evaluations]
                else:
                    metrics_values = [''] * len(experiment.evaluations)

                # Write the row to CSV
                writer.writerow(prompt_data + metrics_values)


class TracerFactory:
    @staticmethod
    def get_tracer(tracer_type: str, trace_target:str) -> Tracer:
        if tracer_type == 'file':
            return FileTracer(trace_target)
        else:
            raise ValueError(f"Unknown tracer: {tracer_type}")