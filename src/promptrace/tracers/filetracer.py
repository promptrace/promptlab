import csv
from datetime import datetime
import os
import uuid
from promptrace.config import EvaluationConfig
from promptrace.tracers.tracer import Tracer

class FileTracer(Tracer):
    def __init__(self, trace_target: str):
        """
        Initialize SQLite tracer.
        
        Args:
            trace_target: Directory path where the file will be stored
        """
        super().__init__(trace_target)
        self.trace_target = trace_target 

    def trace(self, result, evaluations: list[EvaluationConfig]):
        trace_target = self.trace_target.replace("\t", "\\t")
        file_name = datetime.now().strftime("run.%Y%m%d.%H%M%S.txt")
        file_path = os.path.join(trace_target, file_name)

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='|')

            headers = ['exp_id','model_type','model','prompt_template', 'user_prompt','system_prompt', 'dataset', 'inference', 'prompt_token', 'completion_token'] + [evaluation.metric for evaluation in evaluations]
            writer.writerow(headers)
            experiment_id = str(uuid.uuid4())

            for item in result:
                row = [experiment_id]
                # item.insert(0, experiment_id)
                for i in item:
                    row.append(str(i).replace('\n', ' '))
                writer.writerow(row)