import json
import os
import sys
from promptrace import PrompTrace

if __name__ == "__main__":
    test_experiments = {
                "model" : {
                        "type": "azure_openai",
                        "api_key": "", 
                        "api_version": "2024-10-21", 
                        "endpoint": "",
                        "deployment": "gpt-4o"
                },
                "prompt_template": "",
                "dataset": "",
                "evaluation": [
                        {'metric': 'is_numeric'}
                ],    
        }
    tracer = {
        "type": "file",
        "target": ""
    }
    prompt_trace = PrompTrace(tracer)
    prompt_trace.run(test_experiments)
