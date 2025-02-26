from datetime import datetime
import json
from pathlib import Path
import sqlite3
from typing import Dict, List
import uuid
from promptrace.config import ExperimentConfig
from promptrace.enums import AssetType
from promptrace.tracer.tracer import Tracer
from promptrace.utils import sanitize_path

class SQLiteTracer(Tracer):
    
    CREATE_ASSETS_TABLE_QUERY = '''
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id TEXT,
                    asset_type TEXT,
                    asset_name TEXT,
                    asset_binary BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
    CREATE_EXPERIMENTS_TABLE_QUERY = '''
                    CREATE TABLE IF NOT EXISTS experiments (
                        experiment_id TEXT PRIMARY KEY,
                        model BLOB,
                        prompt_template_path TEXT,
                        dataset_path TEXT,
                        asset_id TEXT,
                        is_deployed BOOLEAN DEFAULT 0,
                        deployment_time TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
                    )
                '''
    CREATE_EXPERIMENT_RESULT_TABLE_QUERY = '''
                    CREATE TABLE IF NOT EXISTS experiment_result (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        experiment_id TEXT,
                        dataset_record_id TEXT,
                        inference TEXT,
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        latency_ms REAL,
                        evaluation BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(experiment_id) REFERENCES experiments(experiment_id)
                    )
                '''
    
    INSERT_ASSETS_QUERY = '''INSERT INTO assets(
                                        asset_id, 
                                        asset_type, 
                                        asset_name, 
                                        asset_binary
                                    ) VALUES(?, ?, ?, ?)'''

    INSERT_EXPERIMENT_QUERY = '''
                                INSERT INTO experiments (
                                        experiment_id,
                                        model,
                                        prompt_template_path,
                                        dataset_path,
                                        created_at,
                                        asset_id
                                ) VALUES (?, ?, ?, ?, ?, ?)'''
    
    INSERT_BATCH_EXPERIMENT_RESULT_QUERY = '''
                                INSERT INTO experiment_result (
                                        experiment_id,
                                        dataset_record_id,
                                        inference,
                                        prompt_tokens,
                                        completion_tokens,
                                        latency_ms,
                                        evaluation,
                                        created_at
                                ) VALUES (
                                        :experiment_id,
                                        :dataset_record_id,
                                        :inference,
                                        :prompt_tokens,
                                        :completion_tokens,
                                        :latency_ms,
                                        :evaluation,
                                        :created_at)
            '''
    
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
                self.connection.execute(self.CREATE_EXPERIMENTS_TABLE_QUERY)                
                self.connection.execute(self.CREATE_ASSETS_TABLE_QUERY)                
                self.connection.execute(self.CREATE_EXPERIMENT_RESULT_TABLE_QUERY)                
        except sqlite3.Error as e:
            raise SyntaxError(f"Failed to initialize SQLite database: {str(e)}")

    def trace(self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]) -> None:
        with self.connection:
            timestamp = datetime.now().isoformat()
            asset_id = str(uuid.uuid4())
            experiment_id = str(uuid.uuid4())

            pt_path = experiment_config.prompt_template
            with open(pt_path, 'rb') as file:
                binary = file.read()
            asset_name = Path(pt_path).name

            model = {
                "type": experiment_config.model.type,
                "api_version": experiment_config.model.api_version,
                "endpoint": str(experiment_config.model.endpoint),
                "inference_model_deployment": experiment_config.model.inference_model_deployment,
                "embedding_model_deployment": experiment_config.model.embedding_model_deployment
            }

            self.connection.execute(self.INSERT_ASSETS_QUERY, (asset_id, AssetType.PROMPT_TEMPLATE.value, asset_name, binary))
            self.connection.execute(self.INSERT_EXPERIMENT_QUERY, (experiment_id, json.dumps(model), experiment_config.prompt_template, experiment_config.dataset, timestamp, asset_id))

            for exp in experiment_summary:
                exp['asset_id'] = asset_id

            self.connection.executemany(self.INSERT_BATCH_EXPERIMENT_RESULT_QUERY, experiment_summary)