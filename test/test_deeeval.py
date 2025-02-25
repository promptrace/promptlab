from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
import os
from ragas import SingleTurnSample
from ragas.metrics import AspectCritic
import asyncio
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import LLMContextRecall

os.environ["AZURE_OPENAI_API_KEY"] = "574499b10fea4553ad7a103db3065e4d"

azure_config = {
    "base_url": "https://reteval4254999170.openai.azure.com",  
    "model_deployment": "gpt-4o",  
    "model_name": "gpt-4o",  
    "embedding_deployment": "text-embedding-ada-002",  
    "embedding_name": "text-embedding-ada-002",  
}

evaluator_llm = LangchainLLMWrapper(AzureChatOpenAI(
    openai_api_version="2024-10-21",
    azure_endpoint=azure_config["base_url"],
    azure_deployment=azure_config["model_deployment"],
    model=azure_config["model_name"],
    validate_base_url=False,
))

evaluator_embeddings = LangchainEmbeddingsWrapper(AzureOpenAIEmbeddings(
    openai_api_version="2024-10-21",
    azure_endpoint=azure_config["base_url"],
    azure_deployment=azure_config["embedding_deployment"],
    model=azure_config["embedding_name"],
))

async def main():

    sample = SingleTurnSample(
        user_input="Where is the Eiffel Tower located?",
        response="The Eiffel Tower is located in Paris.",
        reference="The Eiffel Tower is located in Paris.",
        retrieved_contexts=["Paris is the capital of France."], 
    )

    context_recall = LLMContextRecall(llm=evaluator_llm)
    v = await context_recall.single_turn_ascore(sample)

    print(v)

asyncio.run(main())