import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json
import logging
from dataclasses import asdict
import uuid

from promptrace.config import EvaluationConfig
from promptrace.tracers.tracer import Tracer

logger = logging.getLogger(__name__)

class SQLiteTracer(Tracer):
    """SQLite implementation of the Tracer interface."""
    
    def __init__(self, trace_target: str):
        """
        Initialize SQLite tracer.
        
        Args:
            trace_target: Directory path where the SQLite database will be stored
        """
        super().__init__(trace_target)
        trace_target = self.trace_target.replace("\t", "\\t")

        self.db_path = Path(trace_target) / "promptrace.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        """Create database tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Create experiments table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS experiment (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        experiment_id TEXT NOT NULL,
                        model_type TEXT NOT NULL,
                        model_api_version TEXT NOT NULL,
                        model_endpoint TEXT NOT NULL,
                        model_deployment TEXT NOT NULL,                               
                        prompt_template TEXT NOT NULL,
                        system_prompt_template TEXT NOT NULL,
                        user_prompt_template TEXT NOT NULL,                               
                        dataset_path TEXT NOT NULL,
                        dataset_record_id TEXT NOT NULL,
                        inference TEXT NOT NULL,
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        latency_ms REAL,
                        eval blob,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)                     
                
                conn.commit()
                logger.info(f"Initialized SQLite database at {self.db_path}")
                
        except sqlite3.Error as e:
            raise SyntaxError(f"Failed to initialize SQLite database: {str(e)}")

    def trace(self, result: List[Any]) -> None:
        """
        Trace experiment results to SQLite database.
        
        Args:
            experiment: List of experiment results
            evaluations: List of evaluation configurations
        """
        # try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            experiment_id = str(uuid.uuid4())
            
            # Process each result
            for result in result:
                # Insert result record
                cursor.execute("""
                    INSERT INTO experiment (
                        experiment_id,
                        model_type,
                        model_api_version,
                        model_endpoint,
                        model_deployment,                               
                        prompt_template,
                        system_prompt_template,
                        user_prompt_template,                               
                        dataset_path,
                        dataset_record_id,
                        inference,
                        prompt_tokens,
                        completion_tokens,
                        latency_ms,
                        eval
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    experiment_id,
                    result["model_type"],
                    result["model_api_version"],
                    result["model_endpoint"],
                    result["model_deployment"],
                    result["prompt_template"],
                    result["system_prompt"],
                    result["user_prompt"],
                    result["dataset"],
                    result["dataset_record_id"],
                    result["inference"],
                    result["prompt_tokens"],
                    result["completion_tokens"],
                    result["latency_ms"],
                    json.dumps(result["eval"])                    
                ))
            
            conn.commit()