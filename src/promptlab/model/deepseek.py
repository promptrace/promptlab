from openai import OpenAI

from promptlab.model.model import Model
from promptlab.types import InferenceResult


class DeepSeek(Model):
    def __init__(self, api_key, endpoint, deployment):
        self.deployment = deployment
        self.client = OpenAI(api_key=api_key, base_url=str(endpoint))

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