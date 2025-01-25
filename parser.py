import json
import os
from .experiment import Evaluation, Experiment

class Parser:
    @staticmethod
    def parse(json_input: str) -> Experiment:
        experiment = json.loads(json_input)
        cwd = os.getcwd()

        return Experiment(
            prompt_dir=experiment.get("prompt_dir"),
            prompt=experiment.get("prompt"),
            prompt_path=Parser.get_prompt_path(experiment, cwd),
            prompt_version=experiment.get("prompt_version"),
            inputs=experiment.get("inputs"),
            data_dir=experiment.get("data_dir"),
            evaluations=Parser.get_evaluations(experiment)
        )

    @staticmethod
    def get_prompt_path(experiment, cwd):
        prompt_path = os.path.join(cwd, experiment.get("prompt_dir"), experiment.get("prompt"), f'{experiment.get("prompt_version")}.prompty')
        return prompt_path
    
    @staticmethod
    def get_evaluations(experiment):
        evaluations = []
        for evaluation in experiment.get("evaluation"):
            evaluations.append(Evaluation(
                metric=evaluation.get("metric"),
                dataset=evaluation.get("dataset"),
                dataset_version=evaluation.get("dataset_version")
            ))
        return evaluations