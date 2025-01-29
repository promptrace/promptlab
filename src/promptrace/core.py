import os
import uuid
import json

from openai import AzureOpenAI

from promptrace.eval import EvaluationFactory
from promptrace.model import Model
from promptrace.tracer import TracerFactory
from promptrace.parser import Parser
from promptrace.config import ExperimentConfig
from promptrace.parser import Experiment
import os
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any

class ExperimentRunner:

    def run(self, experiment_config: ExperimentConfig):

        experiment = Parser.parse(experiment_config)
        model = Model(model_config=experiment_config.model)
        model.invoke(experiment)
        
        self._run_evaluations(experiment_config, experiment)
        self._trace_results(experiment_config, experiment)
    
    def _run_evaluations(self, experiment_config: ExperimentConfig, experiment: Experiment):
        for evaluation in experiment_config.evaluation:
            evaluator = EvaluationFactory.get_evaluator(evaluation.metric)
            for prompt in experiment.prompts:
                evaluator.evaluate(prompt)
    
    def _trace_results(self, experiment_config: ExperimentConfig, experiment: Experiment):
        tracer = TracerFactory.get_tracer(experiment_config.tracer.type, experiment_config.tracer.target)
        tracer.trace(experiment, experiment_config.model)

class PrompTrace:
    def __init__(self):
        self._config_validator = ExperimentConfigValidator()
        self._runner = None

    def run(self, _experiment: dict):
        experiment_config = self._config_validator.validate(_experiment)

        self._runner = ExperimentRunner()
        
        self._runner.run(experiment_config)

class ExperimentConfigValidator:
    def validate(self, _experiment: dict) -> ExperimentConfig:
        try:
            return ExperimentConfig.model_validate(_experiment)
        except Exception as e:
            raise ValueError(f"Invalid experiment configuration: {str(e)}")