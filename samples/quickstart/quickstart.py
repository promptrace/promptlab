import os
from promptlab import PromptLab
from promptlab.types import Dataset, PromptTemplate

def create_prompt_template(prompt_lab: PromptLab):

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

    prompt_lab.asset.create_or_update(prompt_template) 

def create_dataset(prompt_lab: PromptLab):

    name = "qna_eval_dataset"
    description = "dataset for evaluating the qna prompt.",
    file_path = "C:\work\promptlab\test\dataset\qna.jsonl",

    dataset = Dataset (
        name = name,
        description = description,
        file_path = file_path,
    )

    prompt_lab.asset.create_or_update(dataset) 

def create_experiment(prompt_lab: PromptLab):

    experiment = {
            "model" : {
                    "type": "azure_openai",
                    "api_key": os.environ["azure_openai_key"], 
                    "api_version": "[Azure_Open_AI_API_Version]", 
                    "endpoint": "https://[Azure_Open_AI_Service].openai.azure.com",
                    "inference_model_deployment": "[Inference_Model_Deployment]",
                    "embedding_model_deployment": "[Embedding_Model_Deployment]"
            },
            "prompt_template": {
                "id":"[Prompt_Template_ID]",
                "version": "[Version]"
            },
            "dataset": {
                "id":"[Prompt_Template_ID]",
                "version": "[Version]"
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
                        "metric": "NoiseSensitivity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"answer",
                            "retrieved_contexts":"context",
                            "user_input":"question",
                        },
                    }
                ],    
    }

    prompt_lab.experiment.run(experiment)

def deploy_prompt_template(prompt_lab: PromptLab):
    
    deployment_dir = "c:\prompts"
    prompt = PromptTemplate (
        id='[Prompt_Template_Id]',
        version= '[Prompt_Template_Version]',
        )
    
    prompt_lab.asset.deploy(prompt, deployment_dir)

if __name__ == "__main__":

    tracer_config = {
        "type": "sqlite",
        "db_file": "[DB_Dir]\promptlab.db"
    }
  
    prompt_lab = PromptLab(tracer_config)

    create_prompt_template(prompt_lab)
    
    create_dataset(prompt_lab)

    create_experiment(prompt_lab)

    deploy_prompt_template(prompt_lab)

    prompt_lab.studio.start(8000)


