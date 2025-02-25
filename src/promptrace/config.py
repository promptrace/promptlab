from typing import List

from pydantic import BaseModel, HttpUrl, field_validator

from promptrace.enums import TracerType
from promptrace.utils import sanitize_path

class ModelConfig(BaseModel):
    type: str
    api_key: str
    api_version: str
    endpoint: HttpUrl
    inference_model_deployment: str
    embedding_model_deployment: str

class EvaluationConfig(BaseModel):
    type: str
    metric: str
    column_mapping: dict

class ExperimentConfig(BaseModel):
    model: ModelConfig
    prompt_template: str
    dataset: str
    evaluation: List[EvaluationConfig]

    class Config:
        extra = "forbid" 

    @field_validator('prompt_template')
    def validate_prompt_template(cls, value):             
        return sanitize_path(value)
    
    @field_validator('dataset')
    def validate_dataset(cls, value):             
        return sanitize_path(value)
    
class TracerConfig(BaseModel):
    type: TracerType  
    db_server: str

    @field_validator('db_server')
    def validate_db_server(cls, value):             
        return sanitize_path(value)
    
    class Config:
        use_enum_values = True 

class ConfigValidator:
    @staticmethod
    def validate_tracer_config(tracer_config: dict) -> TracerConfig:
        try:
            return TracerConfig(**tracer_config)
        except Exception as e:
            raise ValueError(f"Invalid tracer configuration: {str(e)}")

    @staticmethod
    def validate_experiment_config(experiment_config: dict) -> ExperimentConfig:
        try:
            return ExperimentConfig(**experiment_config)
        except Exception as e:
            raise ValueError(f"Invalid experiment configuration: {str(e)}")