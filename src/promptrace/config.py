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