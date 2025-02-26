from abc import ABC, abstractmethod
from typing import Dict, List

from promptrace.config import ExperimentConfig

class Tracer(ABC):
    def __init__(self, db_server):
        self.db_server = db_server

    @abstractmethod
    def trace(self,experiment_config: ExperimentConfig, experiment_summary: List[Dict]):
        pass