import os
from datetime import datetime

class Tracer:
    def __init__(self, target: str):
        self.target = target

    def trace_file(self, eval: list):
        file_name = datetime.now().strftime("run.%Y%m%d.%H%M%S.txt")
        eval_file_path = os.path.join(os.getcwd(), self.target, file_name)

        with open(eval_file_path, 'w') as f:
            f.write(f'exp_id\tprompt\tprompt_version\tevaluation_dataset\tevaluation_dataset_version\tevaluation_metric\tevaluation_result\toutput' + '\n')
            for line in eval:
                f.write(line + '\n')