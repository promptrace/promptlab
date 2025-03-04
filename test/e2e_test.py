from promptrace import PrompTrace
from promptrace.types import Dataset, PromptTemplate

if __name__ == "__main__":

    # Create prompt trace object.
    tracer = {
        "type": "sqlite",
        "db_file": "C:\work\promptrace\test\trace_target\promptrace.db"
    }
  
    prompt_trace = PrompTrace(tracer)

    # Create assets.
    system_prompt = "You are a helpful assitant who can extract information from given text."
    user_prompt = '''Here is some information. 
                    <context>

                    Try answering this question.
                    <question>'''
    
    prompt = PromptTemplate (
        name = "question-answering",
        description = "A prompt that can be used for question answering",
        system_prompt = system_prompt,
        user_prompt = user_prompt,
    )

    dataset = Dataset (
        name = "qna_eval",
        description = "qna eval dataset",
        file_path = "C:\work\promptrace\test\dataset\qna.jsonl",
    )
    
    # prompt_trace.asset.create_or_update(prompt)    
    # prompt_trace.asset.create_or_update(dataset)

    # Run experiments.
    experiment = {
            "model" : {
                    "type": "azure_openai",
                    "api_key": "574499b10fea4553ad7a103db3065e4d", 
                    "api_version": "2024-10-21", 
                    "endpoint": "https://reteval4254999170.openai.azure.com",
                    "inference_model_deployment": "gpt-4o",
                    "embedding_model_deployment": "text-embedding-ada-002"
            },
            "prompt_template_id": "1ec94825-a035-4dfd-af13-254df2a40842",
            "dataset_id": "7a1b627e-2d41-47c8-b257-8967b91d4714",
            "evaluation": [
                    {
                        "type": "ragas",
                        "metric": "SemanticSimilarity",
                        "column_mapping": {
                            "response":"answer",
                            "reference":"context"
                        },
                    },
                    {
                        "type": "ragas",
                        "metric": "RougeScore",
                        "column_mapping": {
                            "response":"answer",
                            "reference":"context"
                        },
                    }
                ],    
    }

    # prompt_trace.experiment.run(experiment)

    # Start studio.
    prompt_trace.studio.start(8000)

    # # Deploy asset
    # prompt = PromptTemplate (
    #     id="1ec94825-a035-4dfd-af13-254df2a40842",
    # )
    # prompt_trace.asset.deploy(prompt, "C:\work")
