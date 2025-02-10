from promptrace.config import ModelConfig
from promptrace.enums import ModelType
from promptrace.model.azure_openai import _AzureOpenAI
from promptrace.model.deepseek import DeepSeek
from promptrace.model.model import Model

class ModelFactory:
    @staticmethod
    def get_model(model_config: ModelConfig) -> Model:
        connection_type = model_config.type
        if connection_type == ModelType.AZURE_OPENAI.value:
            return _AzureOpenAI(model_config=model_config)
        if connection_type == ModelType.DEEPSEEK.value:
            return DeepSeek(model_config=model_config)
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")
        
