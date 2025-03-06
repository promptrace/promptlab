import os
from promptrace import PrompTrace
from promptrace.types import Dataset, PromptTemplate

if __name__ == "__main__":

    # Create prompt trace object.
    tracer = {
        "type": "sqlite",
        "db_file": "C:\work\promptrace\test\trace_target\promptrace.db"
    }
  
    prompt_trace = PrompTrace(tracer)

    # # Create assets.
    # system_prompt = "You are a helpful assitant who can extract information from given text."
    # user_prompt = '''Here is some information. 
    #                 <context>

    #                 Try answering this question.
    #                 <question>'''
    
    # prompt = PromptTemplate (
    #     name = "question-answering",
    #     description = "A prompt that can be used for question answering",
    #     system_prompt = system_prompt,
    #     user_prompt = user_prompt,
    # )

    # dataset = Dataset (
    #     name = "qna_eval",
    #     description = "qna eval dataset",
    #     file_path = "C:\work\promptrace\test\dataset\qna.jsonl",
    # )
    
    # prompt_trace.asset.create_or_update(prompt)    
    # prompt_trace.asset.create_or_update(dataset)

    # system_prompt = "You are a helpful assitant who can extract information from given text."
    # user_prompt = '''Here is some information. 
    #                 <context>

    #                 Try answering this question. Dont invent answers, only use the information provided.
    #                 <question>'''
    
    # prompt = PromptTemplate (
    #     id="5f8d28a6-d61f-4154-9e85-60e49c0fd25a",
    #     description = "A prompt that can be used for question answering without hallucination",
    #     system_prompt = system_prompt,
    #     user_prompt = user_prompt,
    # )
    # prompt_trace.asset.create_or_update(prompt)    

    # dataset = Dataset (
    #     id="fe5b1720-4c0d-43b7-9ee7-00317dd0b194",
    #     name = "qna_eval2",
    #     description = "qna eval dataset updated",
    #     file_path = "C:\work\promptrace\test\dataset\qna.jsonl",
    # )
    # prompt_trace.asset.create_or_update(dataset)    

    # Run experiments.
    experiment = {
            "model" : {
                    "type": "azure_openai",
                    "api_key": os.environ["azure_openai_key"], 
                    "api_version": "2024-10-21", 
                    "endpoint": "https://reteval4254999170.openai.azure.com",
                    "inference_model_deployment": "gpt-4o",
                    "embedding_model_deployment": "text-embedding-ada-002"
            },
            "prompt_template": {
                "id":"5f8d28a6-d61f-4154-9e85-60e49c0fd25a",
                "version": "1"
            },
            "dataset": {
                "id":"fe5b1720-4c0d-43b7-9ee7-00317dd0b194",
                "version": "1"
            },
            "evaluation": [
                    {
                        "type": "ragas",
                        "metric": "SemanticSimilarity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"answer"
                        },
                    },
                    {
                        "type": "ragas",
                        "metric": "NoiseSensitivity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"answer",
                            "retrieved_contexts":"context",
                            "user_input":"question",
                        },
                    }
                ],    
    }

    prompt_trace.experiment.run(experiment)

    # # Deploy asset
    # prompt = PromptTemplate (
    #     id="5f8d28a6-d61f-4154-9e85-60e49c0fd25a",
    #     version=2    )
    # prompt_trace.asset.deploy(prompt, "C:\work")

    # Start studio.
    prompt_trace.studio.start(8000)


