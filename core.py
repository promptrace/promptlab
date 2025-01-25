import os
import uuid
import json

from .eval import EvaluationFactory
from .parser import Parser  
from .tracer import Tracer
import prompty
import prompty.azure
from prompty.tracer import trace, console_tracer, PromptyTracer
import os

class PrompTrace:
    def __init__(self, target: str):
        self.target = target

    def run(self, experiments: dict):
        eval = []
        for experiment in experiments:
            exp_id = str(uuid.uuid4())  

            json_input = json.dumps(experiment)
            experiment = Parser.parse(json_input)

            inference_result = prompty.execute(
                prompt=experiment.prompt_path, 
                inputs=experiment.inputs
            )
            inference_result = inference_result.replace('\n', '\\n')
            inference_result = inference_result.replace('\t', ' ')

            for evaluation in experiment.evaluations:
                strategy = EvaluationFactory.get_evaluation_strategy(evaluation.metric)
                evaluation_result = strategy.evaluate(inference_result)
                output = f'{exp_id}\t{experiment.prompt}\t{experiment.prompt_version}\t{evaluation.dataset}\t{evaluation.dataset_version}\t{evaluation.metric}\t{evaluation_result}\t{inference_result}'
                eval.append(output)

        tracer = Tracer(self.target)
        tracer.trace_file(eval)

  

