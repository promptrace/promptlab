## PrompTrace

From building and tracking experiments to productionizing prompts.

## Why PrompTrace

Prompt engineering is often done by software engineers with little to no background in ML or Data Science. PrompTrace is designed to simplify the process, enabling easy experiment setup, prompt evaluation, and production tracking.

Key Benefits:

✅ Easy to adopt – No ML or Data Science expertise required.

✅ Self-contained – No need for additional cloud services for tracking or collaboration.

✅ Seamless integration – Works within your existing web, mobile, or backend project.

## Core Concepts
### Experiment
Experiment is at the center of PrompTrace. An experiment means running a prompt for a dataset and evaluating the outcome against some defined metrics. It is provided as a json file.

Parts of an expriment are -

- Model: Configuration to connect to an LLM endpoint.
- Prompt Template: It is a path for a file which contains the prompt text. The prompt template may include placeholders, which are dynamically replaced with data from a dataset.

    Prompt template format

        <<system>>
        TEXT FOR SYSTEM PROMPT GOES HERE.

        <<user>>
        TEXT FOR USER PROMPT GOES HERE. FOR PLACEHOLDER, USE THIS SYNTAX <PLACEHOLDER>.

    Make sure `<<system>>` and `<<user>>` are written like this. For placeholders, use this syntax `<placeholder>`.
- Dataset: It is a path for a json file which contains the evaluation dataset. 

    Dataset template format

        [
            [
                {"title":"sample_title", "value":"sample_text"}, 
                ...
                ...
                {"title":"sample_title", "value":"sample_text"}
            ],
            [
                {"title":"sample_title", "value":"sample_text"}, 
                ...
                ...
                {"title":"sample_title", "value":"sample_text"}
            ]
        ]
- Evaluation (optional): It is a list of evaluation metrics. 
### Tracer
Tracer stores the experiment output.

## How to use
- Install the `promptrace` library.

        pip install promptrace
- Create a folder for prompt template and store the prompt template there.
- Create a folder for dataset and store the dataset there.

Sample code

```python
import json
from promptrace import PrompTrace

# Define the experiment configuration
experiment_config = {
    "model": {
        "type": "azure_openai",
        "api_key": "your_api_key",
        "api_version": "your_api_version",
        "endpoint": "your_endpoint",
        "deployment": "deployment_name"
    },
    "prompt_template": "prompt_template_path",
    "dataset": "dataset_path",
    "evaluation": [
        {"metric": "metric_name"}
        {"metric": "metric_name"}
    ]
}

# Define the tracer configuration
tracer_config = {
    "type": "tracer_type",
    "target": "target_folder"
}

# Create a PrompTrace instance and run the experiment
prompt_trace = PrompTrace(tracer=tracer_config)
prompt_trace.run(experiment_config)
```

## Samples
[coming soon]