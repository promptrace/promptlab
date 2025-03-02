from pathlib import Path
import sqlite3
from promptrace.config import TracerConfig
from promptrace.enums import TracerType
from promptrace.tracer.sqlite_tracer import SQLiteTracer
from promptrace.tracer.tracer import Tracer


class TracerFactory:
    @staticmethod
    def get_tracer(tracer_type: str, connection: sqlite3.Connection) -> Tracer:
        if tracer_type == TracerType.SQLITE.value:
            return SQLiteTracer(connection)
        else:
            raise ValueError(f"Unknown tracer: {tracer_type}")