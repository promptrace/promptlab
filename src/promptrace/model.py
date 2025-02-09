from openai import AsyncAzureOpenAI, AsyncOpenAI
from promptrace.config import ModelConfig
from dataclasses import dataclass
from promptrace.enums import ModelType

@dataclass
class InferenceResult:
    inference: str
    prompt_tokens: int
    completion_tokens: int

class _AzureOpenAI:
    def __init__(self, api_key, api_version, endpoint, deployment):
        self.deployment = deployment
        self.client = AsyncAzureOpenAI(
            api_key=api_key,  
            api_version=api_version,
            azure_endpoint=str(endpoint)
        )
        
    async def invoke(self, system_prompt: str, user_prompt: str):
        payload = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        chat_completion = await self.client.chat.completions.create(
            model=self.deployment, 
            messages=payload
        )
        inference = chat_completion.choices[0].message.content
        prompt_token = chat_completion.usage.prompt_tokens
        completion_token = chat_completion.usage.completion_tokens

        return InferenceResult(
            inference=inference,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token
        )
       
class DeepSeek:
    def __init__(self, api_key, endpoint, deployment):
        self.deployment = deployment
        self.client = AsyncOpenAI(api_key=api_key, base_url=str(endpoint))

    async def invoke(self, system_prompt: str, user_prompt: str):
        payload = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        chat_completion = await self.client.chat.completions.create(
            model=self.deployment, 
            messages=payload
        )
        inference = chat_completion.choices[0].message.content
        prompt_token = chat_completion.usage.prompt_tokens
        completion_token = chat_completion.usage.completion_tokens

        return InferenceResult(
            inference=inference,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token
        )
    
class ModelFactory:
    @staticmethod
    def get_model(model_config: ModelConfig):
        connection_type = model_config.type
        if connection_type == ModelType.AZURE_OPENAI.value:
            return _AzureOpenAI(model_config.api_key, model_config.api_version, model_config.endpoint, model_config.deployment)
        if connection_type == ModelType.DEEPSEEK.value:
            return DeepSeek(model_config.api_key, model_config.endpoint, model_config.deployment)
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")

class Model:
    def __init__(self, model_config: ModelConfig):
        self.model = ModelFactory.get_model(model_config)

    async def invoke(self, system_prompt: str, user_prompt: str):
        return await self.model.invoke(system_prompt, user_prompt)