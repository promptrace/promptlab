import asyncio
from datetime import datetime
import json
import sqlite3
import uuid
from typing import List, Dict

from promptrace.asset.dataset import Dataset
from promptrace.asset.prompt_template import PromptTemplate
from promptrace.config import ConfigValidator, ExperimentConfig
from promptrace.model.model import Model
from promptrace.model.model_factory import ModelFactory
from promptrace.prompt import Prompt
from promptrace.evaluator.evaluator_factory import EvaluatorFactory
from promptrace.tracer.tracer_factory import TracerFactory
from promptrace.utils import sanitize_path

class Experiment:
    def __init__(self, connection: sqlite3.Connection):
        
        self.connection = connection

    # SELECT_ASSETS_QUERY = '''SELECT asset_name, asset_binary FROM assets WHERE asset_id = ?'''

    # def load_dataset(self, dataset_path: str) -> List[Dict]:
    #     conn = sqlite3.connect(str('C:\work\promptrace\\test\\trace_target\promptrace.db'))
    #     cursor = conn.cursor()
        
    #     cursor.execute(self.SELECT_ASSETS_QUERY,  (dataset_path,))
        
    #     datasets = cursor.fetchall()                    
    #     if datasets:
    #         for asset_name, asset_binary in datasets:
    #             dataset_path = asset_binary
                
    #     cursor.close()
    #     conn.close()

    #     dataset_path = json.loads(dataset_path)
    #     dataset_path = dataset_path['file_path']
    #     dataset_path = sanitize_path(dataset_path)
    #     dataset = []
    #     with open(dataset_path, 'r') as file:
    #         for line in file:
    #             dataset.append(json.loads(line.strip()))
    #     return dataset
    
    def run(self, experiment_config: ExperimentConfig, tracer_config: dict):
        experiment_config = ConfigValidator.validate_experiment_config(experiment_config)
        tracer_config = ConfigValidator.validate_tracer_config(tracer_config)        

        prompt = PromptTemplate.get(sql_connection=self.connection, prompt_template_id=experiment_config.prompt_template)

        inference_model = ModelFactory.get_model(experiment_config.model)

        ds = Dataset.get(sql_connection=self.connection, ds_id=experiment_config.dataset)

        # experiment = Experiment(experiment_config)

        experiment_summary = Experiment.start(inference_model, prompt, ds.ds, experiment_config)

        tracer = TracerFactory.get_tracer(tracer_config.type, self.connection)
        tracer.trace(experiment_config, experiment_summary)
      
    def evaluate(inference: str, row, experiment_config: ExperimentConfig) -> str:
        evaluations = []
        for eval in experiment_config.evaluation:
            evaluator = EvaluatorFactory.get_evaluator(eval.type, eval.metric, experiment_config.model)
            data = dict()
            data["inference"] = inference
            for key, value in eval.column_mapping.items():
                data[key] = row[value]
            evaluation_result = evaluator.evaluate(data)
            evaluations.append({
                "metric": f'{eval.type}-{eval.metric}',
                "result": evaluation_result
            })
        return json.dumps(evaluations)
    
    def start(model: Model, prompt: PromptTemplate, dataset: List[Dict], experiment_config: ExperimentConfig) -> List:
        run_result = []

        experiment_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        for row in dataset:
            system_prompt, user_prompt = prompt.prepare_prompts(row)

            inference_result = model.invoke(system_prompt, user_prompt)
            evaluation = Experiment.evaluate(inference_result.inference, row, experiment_config)

            res = dict()
            res["experiment_id"] = experiment_id
            res["dataset_record_id"] = row['id']
            res["inference"] = inference_result.inference
            res["prompt_tokens"] = inference_result.prompt_tokens
            res["completion_tokens"] = inference_result.completion_tokens
            res["latency_ms"] = inference_result.latency_ms
            res["evaluation"] = evaluation
            res["created_at"] = current_time
            
            run_result.append(res)
        return run_result
