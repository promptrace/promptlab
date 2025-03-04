from promptrace.asset import Asset
from promptrace.experiment import Experiment
from promptrace.studio.studio import Studio
from promptrace.tracer.tracer_factory import TracerFactory
from promptrace.config import ConfigValidator, TracerConfig

class PrompTrace:

    def __init__(self, tracer_config: dict):

        tracer_config = TracerConfig(**tracer_config)
        ConfigValidator.validate_tracer_config(tracer_config) 

        self.tracer = TracerFactory.get_tracer(tracer_config)
        self.tracer.init_db()

        self.asset = Asset(self.tracer)
        self.experiment = Experiment(self.tracer)
        self.studio = Studio(self.tracer)