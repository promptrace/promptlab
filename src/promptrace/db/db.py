from pathlib import Path
import sqlite3
from typing import Dict
from promptrace.config import TracerConfig

def get_db_connection(tracer_config: TracerConfig) -> sqlite3.Connection:
    if tracer_config.type != "sqlite":
        raise ValueError("Unsupported tracer type")
    db_path = Path(tracer_config.db_server)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}")

    return sqlite3.connect(str(db_path))

def insert_or_update(connection: sqlite3.Connection, query: str, params: tuple = ()):
    connection.execute(query, params)
    connection.commit()
    
def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> Dict:
    """Convert database row to dictionary"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_rows(connection: sqlite3.Connection, query: str, params: tuple = ()) -> list:
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    cursor.execute(query, params)
    rows = cursor.fetchall()   

    return rows