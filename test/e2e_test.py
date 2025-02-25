from promptrace import PrompTrace

if __name__ == "__main__":
    tracer = {
        "type": "sqlite",
        "db_server": "C:\work\promptrace\test\trace_target\promptrace.db"
    }
    experiments = {
            "model" : {
                    "type": "azure_openai",
                    "api_key": "574499b10fea4553ad7a103db3065e4d", 
                    "api_version": "2024-10-21", 
                    "endpoint": "https://reteval4254999170.openai.azure.com",
                    "inference_model_deployment": "gpt-4o",
                    "embedding_model_deployment": "text-embedding-ada-002"
            },
            "prompt_template": "C:\work\promptrace\test\prompt_template\mountain_height_v1.prompt",
            "dataset": "C:\work\promptrace\test\dataset\qna.jsonl",
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
    prompt_trace = PrompTrace(tracer)
    # prompt_trace.run(experiments)
    prompt_trace.start_studio(8000)
    # prompt_trace.deploy('59b02064-6b7a-4ca1-b290-67ba51809cf2', "C:\work")
