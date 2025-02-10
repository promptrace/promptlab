import json
import os
import sys
from promptrace import PrompTrace
from promptrace.serving.api import PromptTraceAPI
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    test_experiments = {
                "model" : {
                        "type": "azure_openai",
                        "api_key": os.environ["azure_openai_key"], 
                        "api_version": "2024-10-21", 
                        "endpoint": "https://reteval4254999170.openai.azure.com",
                        "deployment": "gpt-4o"
                },
                "prompt_template": "C:\work\promptrace\test\prompt_template\mountain_height_v1.prompt",
                "dataset": "C:\work\promptrace\test\dataset\mountain_dataset.jsonl",
                "evaluation": [
                        {'metric': 'is_numeric'},
                        {'metric': 'length'}
                ],    
        }
    tracer = {
        "type": "sqlite",
        "target": "C:\work\promptrace\test\trace_target"
    }
    prompt_trace = PrompTrace(tracer)
    # prompt_trace.run(test_experiments)
    prompt_trace.start_web_server("C:\work\promptrace\test\trace_target", 8000)