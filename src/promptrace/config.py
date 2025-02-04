from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import List
from promptrace.enums import TracerType

class ModelConfig(BaseModel):
    type: str
    api_key: str
    api_version: str
    endpoint: HttpUrl
    deployment: str

class EvaluationConfig(BaseModel):
    metric: str

class ExperimentConfig(BaseModel):
    model: ModelConfig
    prompt_template: str
    dataset: str
    evaluation: List[EvaluationConfig]

    class Config:
        extra = "forbid" 

class TracerConfig(BaseModel):
    type: TracerType  
    target: str

    class Config:
        use_enum_values = True 

class ConfigValidator:
    @staticmethod
    def validate_tracer_config(tracer: dict) -> TracerConfig:
        try:
            return TracerConfig(**tracer)
        except Exception as e:
            raise ValueError(f"Invalid tracer configuration: {str(e)}")

    @staticmethod
    def validate_experiment_config(experiment_config: dict) -> ExperimentConfig:
        try:
            return ExperimentConfig(**experiment_config)
        except Exception as e:
            raise ValueError(f"Invalid experiment configuration: {str(e)}")
