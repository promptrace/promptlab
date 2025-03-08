<h4 align="center">
    <img alt="logo" src="src/img/banner.png" style="width: 100%;">
</h4>

## Table of Contents
- [PromptLab](#promptlab)
- [Why PromptLab](#why-promptlab)
- [Core Concepts](#core-concepts)
  - [Asset](#asset)
    - [Prompt Template](#prompt-template)
    - [Dataset](#dataset)
  - [Experiment](#experiment)
  - [Tracer](#tracer)
- [How to use](#how-to-use)
  - [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
- [Samples](#samples)
- [CLI](#cli)

## PromptLab

PromptLab is a free, open-source library that simplifies building applications with LLMs by tackling some key challenges:  

- Designing experiments with any evaluation library  
- Comparing experiments to identify the best prompt  
- Deploying and tracking prompts in production

## Why PromptLab

PromptLab streamlines prompt engineering, making it easy to set up experiments, evaluate prompts, and track them in production.

Key Benefits:

✅ Easy to adopt – No ML or Data Science expertise required.

✅ Self-contained – No need for additional cloud services for tracking or collaboration.

✅ Seamless integration – Works within your existing web, mobile, or backend project.

## Core Concepts
### Asset
Lifecycle of PromptLab starts from assets. Assets are artefacts used to design experiments. Assets are immutable. Once created they can't be changed, any attempt to update will create a new version of the same asset. Versioning starts from 0 and automatically incremented. 

There are two types of assets.

#### Prompt Template
A prompt template is a prompt with or without placeholders. The placeholders are replaced with actual data before sending to LLM. A prompt template has two parts - system prompt and user prompt. The placeholders are marked using `<PLACEHOLDER>`. 

A sample prompt template -

    system_prompt = "You are a helpful assiStant who can answer questions from a given text."
    user_prompt = '''Here are some information. 
                    <context>

                    Answer this questions from the given information.
                    <question>'''

Here, the `<context>` and `<question>` are placeholders which will be replaced by real information and question before sending to LLM.

#### Dataset
A dataset is a jsonl file which is used to run the evaluation. It's mandatory to have an unique `id` column. PromptLab doesn't store the actual data, rather it only stores the metadata (file path, credentails etc.).

### Experiment
Experiment is at the center of PromptLab. An experiment means running a prompt for every record of the dataset and evaluating the outcome against some defined metrics. The dataset is provided as a jsonl file.

Parts of an expriment are:

- Model: Configuration to connect to an LLM endpoint.
- [Prompt Template](#prompt-template)
- [Dataset](#dataset)
- Evaluation: It is a list of evaluation metrics. PromptLab supports and encourages to bring your own library for evaluation metrics.

A sample experiment definition:

    experiment = {
        "model": {
            "type": "<model_type>",
            "api_key": "<your_api_key>",
            "api_version": "<api_version>",
            "endpoint": "<your_model_endpoint>",
            "inference_model_deployment": "<inference_model_name>",
            "embedding_model_deployment": "<embedding_model_name>"
        },
        "prompt_template_id": "<prompt_template_id>",
        "dataset_id": "<dataset_id>",
        "evaluation": [
            {
                "type": "<evaluation_library>",
                "metric": "<metric_name>",
                "column_mapping": {
                    "<evaluator_parameter_name>": "<dataset_column_name>",
                    ...
                    ...
                    "<evaluator_parameter_name>": "<dataset_column_name>"
                }
            }
        ]
    }


### Tracer

Tracer stores the experiment output to a SQLite database file.

## CLI

PromptLab cli reference [coming soon]

- ptrace experiment list
- ptrace experiment run -config exp.json -type sqlite -db c:\projects\chat.db
- ptrace experiment details 
- ptrace experiment details -id <EXP_GUIAD> 
- ptrace experiment deploy -id <EXP_GUIAD>
- ptrace server start -type sqlite -db c:\projects\chat.db

## Samples

[coming soon]