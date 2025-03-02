from abc import ABC, abstractmethod
import sqlite3
from typing import Dict, List

from promptrace.config import ExperimentConfig

class Tracer(ABC):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    @abstractmethod
    def trace(self,experiment_config: ExperimentConfig, experiment_summary: List[Dict]):
        pass