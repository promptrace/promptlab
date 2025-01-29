import json
from openai import AzureOpenAI
from openai import OpenAI
import requests
from promptrace.config import ModelConfig
from promptrace.parser import Experiment

class _AzureOpenAI:
    def __init__(self, api_key, api_version, endpoint, deployment):
        self.deployment = deployment
        self.client = AzureOpenAI(
            api_key=api_key,  
            api_version=api_version,
            azure_endpoint=str(endpoint)
        )

    def invoke(self, experiment: Experiment):
        for prompt in experiment.prompts:
            payload = [
                {
                    "role": "system",
                    "content": prompt.system
                },
                {
                    "role": "user",
                    "content": prompt.user
                }
            ]
            chat_completion = self.client.chat.completions.create(
                model=self.deployment, 
                messages=payload
            )
            prompt.inference = chat_completion.choices[0].message.content
            prompt.prompt_token = chat_completion.usage.prompt_tokens
            prompt.completion_token = chat_completion.usage.completion_tokens

        return experiment
    
class DeepSeek:
    def __init__(self, api_key, endpoint, deployment):
        self.deployment = deployment
        self.client = OpenAI(api_key=api_key, base_url=str(endpoint))

    def invoke(self, experiment: Experiment):
        for prompt in experiment.prompts:
            payload = [
                {
                    "role": "system",
                    "content": prompt.system
                },
                {
                    "role": "user",
                    "content": prompt.user
                }
            ]
            chat_completion = self.client.chat.completions.create(
                model=self.deployment, 
                messages=payload
            )
            prompt.inference = chat_completion.choices[0].message.content
            prompt.prompt_token = chat_completion.usage.prompt_tokens
            prompt.completion_token = chat_completion.usage.completion_tokens

        return experiment
    
class ModelFactory:
    @staticmethod
    def get_model(model_config: ModelConfig):
        connection_type = model_config.type
        if connection_type == "azure_openai":
            return _AzureOpenAI(model_config.api_key, model_config.api_version, model_config.endpoint, model_config.deployment)
        if connection_type == "deepseek":
            return DeepSeek(model_config.api_key, model_config.endpoint, model_config.deployment)
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")

class Model:
    def __init__(self, model_config: ModelConfig):
        self.model = ModelFactory.get_model(model_config)

    def invoke(self, experiment):
        return self.model.invoke(experiment)