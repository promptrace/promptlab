from promptrace import PrompTrace
from promptrace.asset.dataset import Dataset
from promptrace.asset.prompt_template import PromptTemplate

if __name__ == "__main__":
    tracer = {
        "type": "sqlite",
        "db_server": "C:\work\promptrace\test\trace_target\promptrace.db"
    }
  
    prompt_trace = PrompTrace(tracer)

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
        file_path = "C:\work\promptrace\test\dataset\qna.jsonl",
    )
    
    # prompt_trace.asset.create_or_update(prompt)    
    # prompt_trace.asset.create_or_update(dataset)

    experiments = {
            "model" : {
                    "type": "azure_openai",
                    "api_key": "574499b10fea4553ad7a103db3065e4d", 
                    "api_version": "2024-10-21", 
                    "endpoint": "https://reteval4254999170.openai.azure.com",
                    "inference_model_deployment": "gpt-4o",
                    "embedding_model_deployment": "text-embedding-ada-002"
            },
            "prompt_template": "60a30e59-a314-4613-9630-211235406f40",
            "dataset": "23167ebf-ed19-4994-96a8-3b538f89dfc8",
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

# prompt_trace.experiment.run(experiments, tracer_config=tracer)
prompt_trace.start_studio(8000)
# prompt_trace.deploy('59b02064-6b7a-4ca1-b290-67ba51809cf2', "C:\work")
