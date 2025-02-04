from promptrace.enums import TracerType
from promptrace.tracers.filetracer import FileTracer
from promptrace.tracers.sqlite_tracer import SQLiteTracer
from promptrace.tracers.tracer import Tracer

class TracerFactory:
    @staticmethod
    def get_tracer(tracer_type: str, trace_target:str) -> Tracer:
        if tracer_type == TracerType.FILE.value:
            return FileTracer(trace_target)
        elif tracer_type == TracerType.SQLITE.value:
            return SQLiteTracer(trace_target)
        else:
            raise ValueError(f"Unknown tracer: {tracer_type}")