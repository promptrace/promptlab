from pathlib import Path
import sqlite3
from typing import Dict, List
import uuid
from promptrace.enums import AssetType
from promptrace.tracer.tracer import Tracer

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
                        evaluation BLOB,
                        asset_id TEXT,
                        is_deployed BOOLEAN DEFAULT 0,
                        deployment_time TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
                    )
                '''
    
    INSERT_ASSETS_QUERY = '''INSERT INTO assets(asset_id, asset_type, asset_name, asset_binary) VALUES(?, ?, ?, ?)'''

    INSERT_BATCH_EXPERIMENTS_QUERY = '''
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
                                        evaluation,
                                        created_at,
                                        asset_id
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
                                        :evaluation,
                                        :created_at,
                                        :asset_id
                                )
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
        except sqlite3.Error as e:
            raise SyntaxError(f"Failed to initialize SQLite database: {str(e)}")

    def trace(self, experiment_summary: List[Dict]) -> None:
        with self.connection:
            pt_path = experiment_summary[0]['prompt_template_path']
            with open(pt_path, 'rb') as file:
                binary = file.read()
            asset_id = str(uuid.uuid4())
            asset_name = Path(pt_path).name
            self.connection.execute(self.INSERT_ASSETS_QUERY, (asset_id, AssetType.PROMPT_TEMPLATE.value, asset_name, binary))

            for exp in experiment_summary:
                exp['asset_id'] = asset_id

            self.connection.executemany(self.INSERT_BATCH_EXPERIMENTS_QUERY, experiment_summary)