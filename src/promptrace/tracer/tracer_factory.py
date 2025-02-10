from pathlib import Path
from promptrace.config import TracerConfig
from promptrace.enums import TracerType
from promptrace.tracer.sqlite_tracer import SQLiteTracer
from promptrace.tracer.tracer import Tracer


class TracerFactory:
    @staticmethod
    def get_tracer(tracer_config: TracerConfig) -> Tracer:
        db_server = Path(tracer_config.db_server)
        if tracer_config.type == TracerType.SQLITE.value:
            return SQLiteTracer(db_server)
        else:
            raise ValueError(f"Unknown tracer: {tracer_config.type}")