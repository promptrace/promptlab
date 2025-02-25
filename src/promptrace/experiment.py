import asyncio
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
        for row in dataset:
            system_prompt, user_prompt = prompt.prepare_prompts(row)

            inference_result = model.invoke(system_prompt, user_prompt)
            evaluation = self.evaluate(inference_result.inference, row)

            res = dict()
            res["experiment_id"] = experiment_id
            res["model_type"] = self.experiment_config.model.type
            res["model_type"] = self.experiment_config.model.type
            res["model_api_version"] = self.experiment_config.model.api_version
            res["model_endpoint"] = self.experiment_config.model.endpoint.unicode_string()
            res["model_deployment"] = self.experiment_config.model.inference_model_deployment
            res["prompt_template_path"] = self.experiment_config.prompt_template
            res["user_prompt_template"] = user_prompt
            res["system_prompt_template"] = system_prompt
            res["dataset_path"] = self.experiment_config.dataset
            res["dataset_record_id"] = row['id']
            res["inference"] = inference_result.inference
            res["prompt_tokens"] = inference_result.prompt_tokens
            res["completion_tokens"] = inference_result.completion_tokens
            res["latency_ms"] = inference_result.latency_ms
            res["evaluation"] = evaluation
            res["created_at"] = current_time
            
            run_result.append(res)
        return run_result
      
    def evaluate(self, inference: str, row) -> str:
        evaluations = []
        for eval in self.experiment_config.evaluation:
            evaluator = EvaluatorFactory.get_evaluator(eval.type, eval.metric, self.experiment_config.model)
            data = dict()
            data["inference"] = inference
            for key, value in eval.column_mapping.items():
                data[key] = row[value]
            evaluation_result = evaluator.evaluate(data)
            evaluations.append({
                "metric": f'{eval.type}-{eval.metric}',
                "result": evaluation_result
            })
        return json.dumps(evaluations)