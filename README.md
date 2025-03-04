<h4 align="center">
    <img alt="logo" src="src/img/banner.png" style="width: 100%;">
</h4>

## PrompTrace

From building and tracking experiments to productionizing prompts.

## Why PrompTrace

Prompt engineering is often done by software engineers with little to no background in ML or Data Science. PrompTrace is designed to simplify the process, enabling easy experiment setup, prompt evaluation, and production tracking.

Key Benefits:

✅ Easy to adopt – No ML or Data Science expertise required.

✅ Self-contained – No need for additional cloud services for tracking or collaboration.

✅ Seamless integration – Works within your existing web, mobile, or backend project.

## Core Concepts
### Asset
Lifecycle of PrompTrace starts from assets. Assets are artefacts used to design experiments. Assets are immutable. Once created they can't be changed, any attempt to update will create a new version of the same asset. Versioning starts from 0 and automatically incremented. 

There are two types of assets.

#### Prompt Template
A prompt template is a prompt with or without placeholders. The placeholder are replaced with actual data before sending to LLM. A prompt template has two parts - system prompt and user prompt. The placeholders are marked using `< >`. A sample prompt template -

    system_prompt = "You are a helpful assitant who can answer questions from a given text."
    user_prompt = '''Here are some information. 
                    <context>

                    Answer this questions from the given information.
                    <question>'''

Here, the `<context>` and `<question>` are placeholders which will be replaced by real information and question before sending to LLM.

#### Dataset
A dataset is a jsonl file which is used to run the evaluation. It's mandatory to have an unique `id` column. PrompTrace doesn't store the actual data, rather it only stores the metadata (file path, credentails etc.).


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

### Development Setup

PrompTrace uses VS Code's Development Containers for a consistent development environment. This ensures all developers have the same setup with required dependencies and tools.

### Prerequisites
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

Once all are fullfilled, open VSC (dont clone repo yet), then Cmd/Ctrl + Shift + P and search for `Remote-Containers: Clone Repository in Container Volume` to specify the repo, clone it and run the container.


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

## CLI

PrompTrace

- ptrace experiment list
- ptrace experiment run -config exp.json -type sqlite -db c:\projects\chat.db
- ptrace experiment details 
- ptrace experiment details -id <EXP_GUIAD> 
- ptrace experiment deploy -id <EXP_GUIAD>
- ptrace server start -type sqlite -db c:\projects\chat.db