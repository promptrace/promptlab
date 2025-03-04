from promptrace.config import TracerConfig
from promptrace.enums import TracerType
from promptrace.tracer.sqlite_tracer import SQLiteTracer
from promptrace.tracer.tracer import Tracer

class TracerFactory:
    
    @staticmethod
    def get_tracer(tracer_config: TracerConfig) -> Tracer:
        if tracer_config.type == TracerType.SQLITE.value:
            return SQLiteTracer(tracer_config)
        else:
            raise ValueError(f"Unknown tracer: {tracer_config.type}")