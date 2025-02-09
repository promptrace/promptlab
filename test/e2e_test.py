import json
import os
import sys
import asyncio
from promptrace import PrompTrace
from promptrace.serving.api import PromptTraceAPI

async def run_experiment():
    test_experiments = {
        "model": {
            "type": "azure_openai",
            "api_key": "574499b10fea4553ad7a103db3065e4d", 
            "api_version": "2024-10-21", 
            "endpoint": "https://reteval4254999170.openai.azure.com",
            "deployment": "gpt-4o"
        },
        "prompt_template": os.path.join("test", "prompt_template", "mountain_height_v1.prompt"),
        "dataset": os.path.join("test", "dataset", "mountain_dataset.jsonl"),
        "evaluation": [
            {"metric": "is_numeric"},
            {"metric": "length"}
        ]
    }
    
    tracer = {
        "type": "sqlite",
        "target": os.path.join("test", "trace_target")
    }
    
    prompt_trace = PrompTrace(tracer)
    await prompt_trace.run(test_experiments)

def start_web_server():
    prompt_trace = PrompTrace({
        "type": "sqlite",
        "target": os.path.join("test", "trace_target")
    })
    prompt_trace.start_web_server(os.path.join("test", "trace_target"), 8000)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        start_web_server()
    else:
        asyncio.run(run_experiment())

