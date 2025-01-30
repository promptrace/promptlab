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
        with open(dataset_path, 'r') as file:
            dataset = file.read()
        return json.loads(dataset)
    
    def run(self, model: Model, prompt: Prompt) -> List:
        run_result = []
        dataset = self.load_dataset(self.experiment_config.dataset)
        for item in dataset:
            system_prompt, user_prompt = prompt.prepare_prompts(item)
            inference_result = model.invoke(system_prompt, user_prompt)
            evaluations = self.evaluate_prompts(prompt)
            run_result.append([
                self.experiment_config.model.type,
                self.experiment_config.model.deployment,
                self.experiment_config.prompt_template,
                user_prompt,
                system_prompt,
                self.experiment_config.dataset,
                inference_result.inference,
                inference_result.prompt_tokens,
                inference_result.completion_tokens,
                *evaluations
            ])
        return run_result

    def evaluate_prompts(self, prompt: Prompt) -> List:
        return [
            EvaluationFactory.get_evaluator(eval.metric).evaluate(prompt)
            for eval in self.experiment_config.evaluation
        ]