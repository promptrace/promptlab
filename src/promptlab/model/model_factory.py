from promptlab.enums import ModelType
from promptlab.model.azure_openai import AzOpenAI
from promptlab.model.deepseek import DeepSeek
from promptlab.model.model import Model
from promptlab.types import ModelConfig

class ModelFactory:

    @staticmethod
    def get_model(model_config: ModelConfig) -> Model:

        connection_type = model_config.type
        
        if connection_type == ModelType.AZURE_OPENAI.value:
            return AzOpenAI(model_config=model_config)
        if connection_type == ModelType.DEEPSEEK.value:
            return DeepSeek(model_config=model_config)
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")
        
