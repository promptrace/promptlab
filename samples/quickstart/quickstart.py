import os
from promptlab import PromptLab
from promptlab.types import Dataset, PromptTemplate

def create_prompt_lab(tracer_type: str, tracer_db_file_path: str) -> PromptLab:

    tracer_config = {
        "type": tracer_type,
        "db_file": tracer_db_file_path
    }
  
    prompt_lab = PromptLab(tracer_config)

    return prompt_lab

def create_prompt_template(prompt_lab: PromptLab) -> str:

    name = 'qna_prompt'
    description = 'A prompt designed to generate answers that are grounded in the provided information.'
    system_prompt = 'You are a helpful assitant who can extract information from given text.'
    user_prompt = '''Here is some information. 
                    <context>

                    Try answering this question.
                    <question>'''
    
    prompt_template = PromptTemplate (
        name = name,
        description = description,
        system_prompt = system_prompt,
        user_prompt = user_prompt,
    )

    prompt_template = prompt_lab.asset.create_or_update(prompt_template) 

    return (prompt_template.id, prompt_template.version)

def create_dataset(prompt_lab: PromptLab, file_path: str) -> str:

    name = "qna_eval_dataset"
    description = "dataset for evaluating the qna prompt."

    dataset = Dataset (
        name = name,
        description = description,
        file_path = file_path,
    )

    dataset = prompt_lab.asset.create_or_update(dataset) 

    return (dataset.id, dataset.version)

def create_experiment(prompt_lab: PromptLab, endpoint:str, prompt_template_id: str, prompt_template_version: int, dataset_id: str, dataset_version: int):

    experiment = {
            "model" : {
                    "type": "azure_openai",
                    "api_key": os.environ["azure_openai_key"], 
                    "api_version": "2024-10-21", 
                    "endpoint": endpoint,
                    "inference_model_deployment": "gpt-4o",
                    "embedding_model_deployment": "text-embedding-ada-002"
            },
            "prompt_template": {
                "id": prompt_template_id,
                "version": prompt_template_version
            },
            "dataset": {
                "id": dataset_id,
                "version": dataset_version
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
                        "metric": "NonLLMStringSimilarity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"answer",
                        },
                    }
                ],    
    }

    prompt_lab.experiment.run(experiment)

def deploy_prompt_template(prompt_lab: PromptLab, deployment_dir: str, prompt_template_id: str, prompt_template_version: int):
    
    prompt = PromptTemplate (
        id = prompt_template_id,
        version = prompt_template_version,
        )
    
    prompt_lab.asset.deploy(prompt, deployment_dir)

if __name__ == "__main__":

    tracer_type = 'sqlite'
    tracer_db_file_path = 'C:\work\promptlab\test\trace_target\promptlab.db'
    eval_dataset_file_path = 'C:\work\promptlab\test\dataset\qna.jsonl'
    aoai_endpoint = 'https://reteval4254999170.openai.azure.com'
    deployment_dir = 'C:\work\prompt_templates'

    # Create prompt_lab object which will be used to access different functionalities of the library.
    prompt_lab = create_prompt_lab(tracer_type, tracer_db_file_path)

    # Create a prompt template.
    prompt_template_id, prompt_template_version = create_prompt_template(prompt_lab)
    
    # Create a dataset.
    dataset_id, dataset_version = create_dataset(prompt_lab, eval_dataset_file_path)

    # Let's launch the studio and check the prompt template and dataset.
    prompt_lab.studio.start(8000)

    # Create an experiment and run it.
    create_experiment(prompt_lab, aoai_endpoint, prompt_template_id, prompt_template_version, dataset_id, dataset_version)

    # Let's launch the studio again and check the experiment and its result.
    prompt_lab.studio.start(8000)

    # Let's deploy the prompt template to a directory in production.
    deploy_prompt_template(prompt_lab, deployment_dir, prompt_template_id, prompt_template_version)



