import sqlite3
from typing import Dict, List, Any
import json
import logging
import uuid
from promptrace.tracer.tracer import Tracer

logger = logging.getLogger(__name__)

class SQLiteTracer(Tracer):
    
    def __init__(self, db_server: str):
        """
        Initialize SQLite tracer.
        
        Args:
            db_server: File path of the SQLite database file.
        """
        super().__init__(db_server)
        self.db_path = self.db_server
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)

        self._initialize_database()

    def _initialize_database(self):
        """Create database tables if they don't exist."""
        try:
            with self.connection:
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS experiments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        experiment_id TEXT,
                        model_type TEXT,
                        model_api_version TEXT,
                        model_endpoint TEXT,
                        model_deployment TEXT,
                        prompt_template_path TEXT,
                        system_prompt_template TEXT,
                        user_prompt_template TEXT,
                        dataset_path TEXT,
                        dataset_record_id TEXT,
                        inference TEXT,
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        latency_ms REAL,
                        evaluation TEXT
                    )
                ''')                
        except sqlite3.Error as e:
            raise SyntaxError(f"Failed to initialize SQLite database: {str(e)}")

    def trace(self, experiment_summary: List[Dict]) -> None:
        with self.connection:
            self.connection.executemany('''
                INSERT INTO experiments (
                        experiment_id,
                        model_type,
                        model_api_version,
                        model_endpoint,
                        model_deployment,                               
                        prompt_template_path,
                        system_prompt_template,
                        user_prompt_template,                               
                        dataset_path,
                        dataset_record_id,
                        inference,
                        prompt_tokens,
                        completion_tokens,
                        latency_ms,
                        evaluation
                ) VALUES (
                        :experiment_id,
                        :model_type,
                        :model_api_version,
                        :model_endpoint,
                        :model_deployment,                               
                        :prompt_template_path,
                        :system_prompt_template,
                        :user_prompt_template,                               
                        :dataset_path,
                        :dataset_record_id,
                        :inference,
                        :prompt_tokens,
                        :completion_tokens,
                        :latency_ms,
                        :evaluation
                )
            ''', experiment_summary)
        # with sqlite3.connect(self.db_path) as conn:
        #     cursor = conn.cursor()
        #     experiment_id = str(uuid.uuid4())
            
        #     for result in experiment_summary:
        #         cursor.execute("""
        #             INSERT INTO experiment (
        #                 experiment_id,
        #                 model_type,
        #                 model_api_version,
        #                 model_endpoint,
        #                 model_deployment,                               
        #                 prompt_template_path,
        #                 system_prompt_template,
        #                 user_prompt_template,                               
        #                 dataset_path,
        #                 dataset_record_id,
        #                 inference,
        #                 prompt_tokens,
        #                 completion_tokens,
        #                 latency_ms,
        #                 evaluation
        #             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        #         """, (
        #             experiment_id,
        #             result["model_type"],
        #             result["model_api_version"],
        #             result["model_endpoint"],
        #             result["model_deployment"],
        #             result["prompt_template"],
        #             result["system_prompt"],
        #             result["user_prompt"],
        #             result["dataset"],
        #             result["dataset_record_id"],
        #             result["inference"],
        #             result["prompt_tokens"],
        #             result["completion_tokens"],
        #             result["latency_ms"],
        #             json.dumps(result["eval"])                    
        #         ))
            
        #     conn.commit()