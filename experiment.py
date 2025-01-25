from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Evaluation:
    metric: str
    dataset: str
    dataset_version: str

@dataclass
class Experiment:
    prompt_dir: str
    prompt: str
    prompt_path: str
    prompt_version: str
    inputs: str
    data_dir: str
    evaluations: List[Evaluation]