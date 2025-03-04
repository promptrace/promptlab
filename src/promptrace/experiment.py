from datetime import datetime
from typing import List, Dict, Tuple
import json
import re
import uuid

from promptrace.config import ConfigValidator, ExperimentConfig
from promptrace.db.sql import SQLQuery
from promptrace.model.model_factory import ModelFactory
from promptrace.evaluator.evaluator_factory import EvaluatorFactory
from promptrace.tracer.tracer import Tracer
from promptrace.utils import Utils

class Experiment:
    def __init__(self, tracer: Tracer):        
        self.tracer = tracer
    
    def run(self, experiment_config: ExperimentConfig):

        experiment_config = ExperimentConfig(**experiment_config)
        ConfigValidator.validate_experiment_config(experiment_config)

        prompt_template = self.tracer.db_client.fetch_data(SQLQuery.SELECT_ASSET_QUERY, (experiment_config.prompt_template_id,))[0]
        system_prompt, user_prompt, prompt_template_variables = self.split_prompt_template(prompt_template)
        
        eval_dataset_path = self.tracer.db_client.fetch_data(SQLQuery.SELECT_DATASET_FILE_PATH_QUERY, (experiment_config.dataset_id,))[0]
        eval_dataset = Utils.load_dataset(eval_dataset_path['file_path'])

        exp_summary = self.init_batch_eval(eval_dataset, system_prompt, user_prompt, prompt_template_variables, experiment_config)

        self.tracer.trace(experiment_config, exp_summary)

    def init_batch_eval(self, eval_dataset, system_prompt, user_prompt, prompt_template_variables, experiment_config: ExperimentConfig) -> List:

        inference_model = ModelFactory.get_model(experiment_config.model)
        experiment_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        exp_summary = []

        for eval_record in eval_dataset:
            system_prompt, user_prompt = self.prepare_prompts(eval_record, system_prompt, user_prompt, prompt_template_variables)

            inference_result = inference_model.invoke(system_prompt, user_prompt)
            evaluation = self.evaluate(inference_result.inference, eval_record, experiment_config)

            eval = dict()
            eval["experiment_id"] = experiment_id
            eval["dataset_record_id"] = eval_record['id']
            eval["inference"] = inference_result.inference
            eval["prompt_tokens"] = inference_result.prompt_tokens
            eval["completion_tokens"] = inference_result.completion_tokens
            eval["latency_ms"] = inference_result.latency_ms
            eval["evaluation"] = evaluation
            eval["created_at"] = timestamp
            
            exp_summary.append(eval)

        return exp_summary
    
    def split_prompt_template(self, asset: Dict) -> Tuple[str, str, List[str]]:
        
        pattern = r'<<system>>\s*(.*?)\s*<<user>>\s*(.*?)\s*(?=<<|$)'    
        matches = re.findall(pattern, asset['asset_binary'], re.DOTALL)
        
        if not matches:
            raise ValueError("No valid prompt format found in template")
            
        system_prompt = matches[0][0].strip()
        user_prompt = matches[0][1].strip()

        system_prompt_varaibles = re.findall(r'<(.*?)>', system_prompt)
        user_prompt_varaibles = re.findall(r'<(.*?)>', user_prompt)
        prompt_template_variables = system_prompt_varaibles + user_prompt_varaibles
        prompt_template_variables = list(set(prompt_template_variables))

        return system_prompt, user_prompt, prompt_template_variables

    def evaluate(self, inference: str, row, experiment_config: ExperimentConfig) -> str:

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
    
    def prepare_prompts(self, item, system_prompt, user_prompt, prompt_template_variables):

        for variable in prompt_template_variables:
            placeholder = f'<{variable}>'
            replacement = f'<{item[variable]}>'

            system_prompt = system_prompt.replace(placeholder, replacement)
            user_prompt = user_prompt.replace(placeholder, replacement)

        return system_prompt, user_prompt