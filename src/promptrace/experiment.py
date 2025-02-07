import json
import asyncio
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
    
    async def process_item(self, item: Dict, model: Model, prompt: Prompt) -> Dict:
        system_prompt, user_prompt = prompt.prepare_prompts(item)
        inference_result = await model.invoke(system_prompt, user_prompt)  # Model.invoke needs to be async too
        evaluation = self.evaluate_prompts(prompt)

        return {
            "model_type": self.experiment_config.model.type,
            "model_api_version": self.experiment_config.model.api_version,
            "model_endpoint": self.experiment_config.model.endpoint.unicode_string(),
            "model_deployment": self.experiment_config.model.deployment,
            "prompt_template": self.experiment_config.prompt_template,
            "user_prompt": user_prompt,
            "system_prompt": system_prompt,
            "dataset": self.experiment_config.dataset,
            "dataset_record_id": self.get_id(item),
            "inference": inference_result.inference,
            "prompt_tokens": inference_result.prompt_tokens,
            "completion_tokens": inference_result.completion_tokens,
            "latency_ms": '-',
            "eval": evaluation,
        }

    async def run(self, model: Model, prompt: Prompt) -> List:
        dataset = self.load_dataset(self.experiment_config.dataset)
        tasks = [self.process_item(item, model, prompt) for item in dataset]
        return await asyncio.gather(*tasks)

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