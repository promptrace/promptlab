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
                        output TEXT NOT NULL,
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

    def trace(self, result: List[Any], evaluations: List[EvaluationConfig]) -> None:
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
                        dataset_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    experiment_id,
                    result[0],
                    '-',
                    '-',
                    result[1],
                    result[2],
                    result[3],
                    result[5],
                    result[4]
                ))
                
                # result_id = cursor.lastrowid
                
                # # Insert evaluation results
                # for eval_config in evaluations:
                #     metric_value = result.get(eval_config.metric, 0.0)
                #     cursor.execute("""
                #         INSERT INTO evaluations (
                #             result_id, metric_name, metric_value
                #         ) VALUES (?, ?, ?)
                #     """, (
                #         result_id,
                #         eval_config.metric,
                #         metric_value
                #     ))
                
                # # Insert metadata if any
                # if 'metadata' in result:
                #     self._insert_metadata(
                #         cursor,
                #         str(result_id),
                #         'result',
                #         result['metadata']
                #     )
            
            conn.commit()
            
        # except sqlite3.Error as e:
        #     raise SyntaxError(f"Failed to trace results to SQLite database: {str(e)}")

    # def _insert_metadata(
    #     self,
    #     cursor: sqlite3.Cursor,
    #     reference_id: str,
    #     reference_type: str,
    #     metadata: Dict[str, Any]
    # ) -> None:
    #     """Insert metadata key-value pairs."""
    #     for key, value in metadata.items():
    #         cursor.execute("""
    #             INSERT INTO metadata (reference_id, reference_type, key, value)
    #             VALUES (?, ?, ?, ?)
    #         """, (
    #             reference_id,
    #             reference_type,
    #             key,
    #             json.dumps(value) if isinstance(value, (dict, list)) else str(value)
    #         ))

    # def query_results(
    #     self,
    #     experiment_id: str = None,
    #     metric_name: str = None,
    #     limit: int = 100
    # ) -> List[Dict[str, Any]]:
    #     """
    #     Query results from the database.
        
    #     Args:
    #         experiment_id: Optional experiment ID to filter by
    #         metric_name: Optional metric name to filter by
    #         limit: Maximum number of results to return
            
    #     Returns:
    #         List of result dictionaries
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             conn.row_factory = sqlite3.Row
    #             cursor = conn.cursor()
                
    #             query = """
    #                 SELECT 
    #                     r.*, 
    #                     e.metric_name,
    #                     e.metric_value,
    #                     exp.model_type,
    #                     exp.model_deployment
    #                 FROM results r
    #                 JOIN experiments exp ON r.experiment_id = exp.experiment_id
    #                 LEFT JOIN evaluations e ON r.result_id = e.result_id
    #                 WHERE 1=1
    #             """
    #             params = []
                
    #             if experiment_id:
    #                 query += " AND r.experiment_id = ?"
    #                 params.append(experiment_id)
                
    #             if metric_name:
    #                 query += " AND e.metric_name = ?"
    #                 params.append(metric_name)
                
    #             query += f" LIMIT {limit}"
                
    #             cursor.execute(query, params)
    #             return [dict(row) for row in cursor.fetchall()]
                
    #     except sqlite3.Error as e:
    #         raise TracingError(f"Failed to query results from SQLite database: {str(e)}")

    # def get_experiment_summary(self, experiment_id: str) -> Dict[str, Any]:
        # """
        # Get summary statistics for an experiment.
        
        # Args:
        #     experiment_id: ID of the experiment
            
        # Returns:
        #     Dictionary containing experiment summary
        # """
        # try:
        #     with sqlite3.connect(self.db_path) as conn:
        #         conn.row_factory = sqlite3.Row
        #         cursor = conn.cursor()
                
        #         # Get experiment details
        #         cursor.execute("""
        #             SELECT * FROM experiments WHERE experiment_id = ?
        #         """, (experiment_id,))
        #         experiment = dict(cursor.fetchone())
                
        #         # Get evaluation metrics
        #         cursor.execute("""
        #             SELECT 
        #                 e.metric_name,
        #                 AVG(e.metric_value) as mean,
        #                 MIN(e.metric_value) as min,
        #                 MAX(e.metric_value) as max
        #             FROM evaluations e
        #             JOIN results r ON e.result_id = r.result_id
        #             WHERE r.experiment_id = ?
        #             GROUP BY e.metric_name
        #         """, (experiment_id,))
        #         metrics = {
        #             row['metric_name']: {
        #                 'mean': row['mean'],
        #                 'min': row['min'],
        #                 'max': row['max']
        #             }
        #             for row in cursor.fetchall()
        #         }
                
        #         # Get token usage
        #         cursor.execute("""
        #             SELECT 
        #                 COUNT(*) as total_samples,
        #                 SUM(total_tokens) as total_tokens,
        #                 AVG(duration_ms) as avg_duration
        #             FROM results
        #             WHERE experiment_id = ?
        #         """, (experiment_id,))
        #         stats = dict(cursor.fetchone())
                
        #         return {
        #             **experiment,
        #             'metrics': metrics,
        #             'statistics': stats
        #         }
                
        # except sqlite3.Error as e:
        #     raise TracingError(
        #         f"Failed to get experiment summary from SQLite database: {str(e)}"
        #     ) 