from pydantic import BaseModel, HttpUrl
from typing import List

class ModelConfig(BaseModel):
    type: str
    api_key: str
    api_version: str
    endpoint: HttpUrl
    deployment: str

class EvaluationConfig(BaseModel):
    metric: str

class TracerConfig(BaseModel):
    type: str
    target: str

class ExperimentConfig(BaseModel):
    model: ModelConfig
    prompt_template: str
    dataset: str
    evaluation: List[EvaluationConfig]
    tracer: TracerConfig

    class Config:
        extra = "forbid" 