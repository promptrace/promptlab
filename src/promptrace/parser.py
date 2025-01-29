import json
import os
import uuid
from promptrace.config import ExperimentConfig
from dataclasses import dataclass
import re
from typing import List, Dict

@dataclass
class Prompt:
    system: str
    user: str
    inference: str = None
    prompt_token: int = 0
    completion_token: int = 0
    evaluation_result: Dict[str, str] = None

@dataclass
class Evaluation:
    metric: str

@dataclass
class Experiment:
    experiment_id: str
    prompt_template: str
    dataset:str
    prompts: List[Prompt]
    evaluations: List[Evaluation]

class Parser:
    @staticmethod
    def parse(experiment_config: ExperimentConfig) -> Experiment:

        return Experiment(
            experiment_id=str(uuid.uuid4()),
            prompt_template = experiment_config.prompt_template,
            dataset=experiment_config.dataset,
            prompts=Parser.get_prompt(experiment_config),
            evaluations=Parser.get_evaluations(experiment_config)
        )

    @staticmethod
    def get_prompt(experiment_config: ExperimentConfig) -> List[Prompt]:

        dataset_path = experiment_config.dataset
        with open(dataset_path, 'r') as file:
            dataset = file.read()
        dataset = json.loads(dataset)

        with open(experiment_config.prompt_template, 'r') as file:
            prompt_content = file.read()

        pattern = r'<<system>>\s*(.*?)\s*<<user>>\s*(.*?)\s*(?=<<|$)'    
        matches = re.findall(pattern, prompt_content, re.DOTALL)        
        system_content = matches[0][0].strip()
        user_content = matches[0][1].strip()

        prompts = []
        for dataset_line in dataset:
            _system_content = system_content
            _user_content = user_content
            for dataset_content in dataset_line:
                _system_content = _system_content.replace(f'<{dataset_content["title"]}>', f'<{dataset_content["value"]}>')
                _user_content = _user_content.replace(f'<{dataset_content["title"]}>', f'<{dataset_content["value"]}>')
            
            prompts.append(Prompt(
                system=_system_content,
                user=_user_content
            ))

        return prompts
            
    @staticmethod
    def get_evaluations(experiment_config: ExperimentConfig) -> List[Evaluation]:
        evaluations = []
        for evaluation in experiment_config.evaluation:
            evaluations.append(Evaluation(
                metric=evaluation.metric,
            ))
        return evaluations