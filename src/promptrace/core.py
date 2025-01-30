import os
import uuid
import json
from pathlib import Path

from openai import AzureOpenAI

from promptrace.eval import EvaluationFactory
from promptrace.experiment import Experiment
from promptrace.model import Model
from promptrace.prompt import Prompt
from promptrace.tracer import TracerFactory
from promptrace.config import ExperimentConfig, TracerConfig
import os
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any
    
class PrompTrace:
    def __init__(self, tracer: dict):
        self.tracer = self.validate_tracer_config(tracer)
    
    def validate_tracer_config(self, tracer: dict) -> TracerConfig:
        try:
            return TracerConfig.model_validate(tracer)
        except Exception as e:
            raise ValueError(f"Invalid tracer configuration: {str(e)}")

    def validate_experiment_config(self, experiment_config: dict) -> ExperimentConfig:
        try:
            return ExperimentConfig.model_validate(experiment_config)
        except Exception as e:
            raise ValueError(f"Invalid experiment configuration: {str(e)}")

    def run(self, _experiment_config: dict):
        self.experiment_config = self.validate_experiment_config(_experiment_config)
        
        model = Model(model_config=self.experiment_config.model)
        prompt = Prompt(prompt_template=self.experiment_config.prompt_template)

        experiment = Experiment(self.experiment_config)
        run_result = experiment.run(model, prompt)

        tracer = TracerFactory.get_tracer(self.tracer.type, self.tracer.target)
        tracer.trace(run_result, self.experiment_config.evaluation)
        
