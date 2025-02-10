from datetime import datetime
import json
import uuid
from typing import List, Dict

from promptrace.config import ExperimentConfig
from promptrace.model.model import Model
from promptrace.prompt import Prompt
from promptrace.evaluator.evaluator_factory import EvaluatorFactory

class Experiment:
    def __init__(self, experiment_config: ExperimentConfig):
        self.experiment_config = experiment_config

    def load_dataset(self, dataset_path: str) -> List[Dict]:
        dataset = []
        with open(dataset_path, 'r') as file:
            for line in file:
                dataset.append(json.loads(line.strip()))
        return dataset
    
    def start(self, model: Model, prompt: Prompt) -> List:
        run_result = []
        dataset = self.load_dataset(self.experiment_config.dataset)

        experiment_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        for item in dataset:
            system_prompt, user_prompt = prompt.prepare_prompts(item)

            inference_result = model.invoke(system_prompt, user_prompt)
            evaluation = self.evaluate(inference_result.inference, item)

            res = dict()
            res["experiment_id"] = experiment_id
            res["model_type"] = self.experiment_config.model.type
            res["model_type"] = self.experiment_config.model.type
            res["model_api_version"] = self.experiment_config.model.api_version
            res["model_endpoint"] = self.experiment_config.model.endpoint.unicode_string()
            res["model_deployment"] = self.experiment_config.model.deployment
            res["prompt_template_path"] = self.experiment_config.prompt_template
            res["user_prompt_template"] = user_prompt
            res["system_prompt_template"] = system_prompt
            res["dataset_path"] = self.experiment_config.dataset
            res["dataset_record_id"] = item['id']
            res["inference"] = inference_result.inference
            res["prompt_tokens"] = inference_result.prompt_tokens
            res["completion_tokens"] = inference_result.completion_tokens
            res["latency_ms"] = inference_result.latency_ms
            res["evaluation"] = evaluation
            res["created_at"] = current_time
            
            run_result.append(res)
        return run_result
      
    def evaluate(self, inference: str, item) -> str:
        evaluations = []
        for metric in self.experiment_config.evaluation:
            evaluator = EvaluatorFactory.get_evaluator(metric)
            
            expected_value = item[metric] if metric in item else None
            evaluation_result = evaluator.evaluate(inference, expected_value)
            evaluations.append({
                "metric": metric,
                "result": evaluation_result
            })
        return json.dumps(evaluations)