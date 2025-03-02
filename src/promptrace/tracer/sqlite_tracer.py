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
from promptrace.db.sql_query import SQLQuery

class SQLiteTracer(Tracer):
    
    def __init__(self, connection: sqlite3.Connection):

        super().__init__(connection)

    def trace(self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]) -> None:
        with self.connection:
            timestamp = datetime.now().isoformat()
            experiment_id = str(uuid.uuid4())

            model = {
                "type": experiment_config.model.type,
                "api_version": experiment_config.model.api_version,
                "endpoint": str(experiment_config.model.endpoint),
                "inference_model_deployment": experiment_config.model.inference_model_deployment,
                "embedding_model_deployment": experiment_config.model.embedding_model_deployment
            }

            asset = {
                "prompt_template_id": experiment_config.prompt_template,
                "dataset_id": experiment_config.dataset
            }

            self.connection.execute(SQLQuery.INSERT_EXPERIMENT_QUERY, (experiment_id, json.dumps(model), json.dumps(asset),0, None, timestamp))

            for exp in experiment_summary:
                exp['experiment_id'] = experiment_id

            self.connection.executemany(SQLQuery.INSERT_BATCH_EXPERIMENT_RESULT_QUERY, experiment_summary)