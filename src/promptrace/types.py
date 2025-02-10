from dataclasses import dataclass

@dataclass
class InferenceResult:
    inference: str
    prompt_tokens: int
    completion_tokens: int