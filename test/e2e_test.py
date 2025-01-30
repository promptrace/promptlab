import json
import os
import sys
from promptrace.core import PrompTrace

if __name__ == "__main__":
    test_experiments = {
                "model" : {
                        "type": "azure_openai",
                        "api_key": "", 
                        "api_version": "2024-10-21", 
                        "endpoint": "",
                        "deployment": "gpt-4o"
                },
                "prompt_template": r"C:\work\promptrace\test\prompt_template\mountain_height_v1.prompt",
                "dataset": r"C:\work\promptrace\test\dataset\mountain_dataset.jsonl",
                "evaluation": [
                        {'metric': 'is_numeric'}
                ],    
        }
    tracer = {
        "type": "file",
        "target": r"C:\work\promptrace\test\trace_target"
    }
    prompt_trace = PrompTrace(tracer)
    prompt_trace.run(test_experiments)
