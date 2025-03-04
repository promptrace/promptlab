import os

from promptrace.evaluator.evaluator import Evaluator
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import RougeScore
from ragas.metrics import SemanticSimilarity
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

from promptrace.types import ModelConfig

class RagasSemanticSimilarity(Evaluator):

    def __init__(self, model: ModelConfig):

        super().__init__(model)

        os.environ["AZURE_OPENAI_API_KEY"] = model.api_key

        self.evaluator_llm = LangchainLLMWrapper(AzureChatOpenAI(
            openai_api_version=self.model.api_version,
            azure_endpoint=str(self.model.endpoint),
            azure_deployment=self.model.inference_model_deployment,
            model=self.model.inference_model_deployment,
            validate_base_url=False,
        ))

        self.evaluator_embeddings = LangchainEmbeddingsWrapper(AzureOpenAIEmbeddings(
            openai_api_version=self.model.api_version,
            azure_endpoint=str(self.model.endpoint),
            azure_deployment=self.model.embedding_model_deployment,
            model=self.model.embedding_model_deployment,
        ))

    def evaluate(self, data: dict) -> str:

        sample = SingleTurnSample(
            response=data["response"],
            reference=data["reference"]
        )

        scorer = SemanticSimilarity(embeddings=LangchainEmbeddingsWrapper(self.evaluator_embeddings))
        val = scorer.single_turn_score(sample)        

        return val
    
class RagasRougeScore(Evaluator):

    def __init__(self, model: ModelConfig):

        super().__init__(model)

        os.environ["AZURE_OPENAI_API_KEY"] = model.api_key

        self.evaluator_llm = LangchainLLMWrapper(AzureChatOpenAI(
            openai_api_version=self.model.api_version,
            azure_endpoint=str(self.model.endpoint),
            azure_deployment=self.model.inference_model_deployment,
            model=self.model.inference_model_deployment,
            validate_base_url=False,
        ))

        self.evaluator_embeddings = LangchainEmbeddingsWrapper(AzureOpenAIEmbeddings(
            openai_api_version=self.model.api_version,
            azure_endpoint=str(self.model.endpoint),
            azure_deployment=self.model.embedding_model_deployment,
            model=self.model.embedding_model_deployment,
        ))
    
    def evaluate(self, data: dict) -> str:
        
        sample = SingleTurnSample(
            response=data["response"],
            reference=data["reference"]
        )

        scorer = RougeScore()
        val = (scorer.single_turn_score(sample))
        
        return val