from abc import ABC, abstractmethod

class Tracer(ABC):
    def __init__(self, db_server):
        self.db_server = db_server

    @abstractmethod
    def trace(self, experiment_summary):
        pass