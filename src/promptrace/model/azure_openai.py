from openai import AzureOpenAI
from promptrace.model.model import Model
from promptrace.config import ModelConfig
from promptrace.types import InferenceResult


class _AzureOpenAI(Model):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)

        self.model_config = model_config
        self.client = AzureOpenAI(
            api_key=model_config.api_key,  
            api_version=model_config.api_version,
            azure_endpoint=str(model_config.endpoint)
        )
        
    def invoke(self, system_prompt: str, user_prompt: str):
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
        chat_completion = self.client.chat.completions.create(
            model=self.model_config.deployment, 
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