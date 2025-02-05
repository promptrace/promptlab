import json
from typing import List, Dict
from promptrace.config import ExperimentConfig
from promptrace.model import Model
from promptrace.prompt import Prompt
from promptrace.eval import EvaluationFactory

class Experiment:
    def __init__(self, experiment_config: ExperimentConfig):
        self.experiment_config = experiment_config

    def load_dataset(self, dataset_path: str) -> List[Dict]:
        dataset_path = dataset_path.replace("\t", "\\t")
        with open(dataset_path, 'r') as file:
            dataset = file.read()
        return json.loads(dataset)
    
    def run(self, model: Model, prompt: Prompt) -> List:
        run_result = []
        dataset = self.load_dataset(self.experiment_config.dataset)
        for item in dataset:
            system_prompt, user_prompt = prompt.prepare_prompts(item)
            inference_result = model.invoke(system_prompt, user_prompt)
            evaluation = self.evaluate_prompts(prompt)

            res = dict()
            res["model_type"] = self.experiment_config.model.type
            res["model_type"] = self.experiment_config.model.type
            res["model_api_version"] = self.experiment_config.model.api_version
            res["model_endpoint"] = self.experiment_config.model.endpoint.unicode_string()
            res["model_deployment"] = self.experiment_config.model.deployment
            res["prompt_template"] = self.experiment_config.prompt_template
            res["user_prompt"] = user_prompt
            res["system_prompt"] = system_prompt
            res["dataset"] = self.experiment_config.dataset
            res["dataset_record_id"] = self.get_id(item)
            res["inference"] = inference_result.inference
            res["prompt_tokens"] = inference_result.prompt_tokens
            res["completion_tokens"] = inference_result.completion_tokens
            res["latency_ms"] = '-'
            res["eval"] = evaluation
            
            run_result.append(res)
        return run_result

    def get_id(self, item):
        for item_part in item:
            if item_part["title"] == "id":
                return item_part["value"]
        return None
        
    def evaluate_prompts(self, prompt: Prompt) -> str:
        evaluations = []
        for eval_config in self.experiment_config.evaluation:
            evaluator = EvaluationFactory.get_evaluator(eval_config.metric)
            evaluation_result = evaluator.evaluate(prompt)
            evaluations.append({
                "metric": eval_config.metric,
                "result": evaluation_result
            })
        return json.dumps(evaluations)