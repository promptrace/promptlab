from pathlib import Path
import sqlite3
from flask import Flask, jsonify
from typing import List, Dict, Any
import logging
from datetime import datetime

from flask_cors import CORS

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "promptrace.db"):
        db_path = db_path.replace("\t", "\\t")
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")
    
    def get_connection(self):
        return sqlite3.connect(str(self.db_path))
    
    def dict_factory(self, cursor: sqlite3.Cursor, row: tuple) -> Dict:
        """Convert database row to dictionary"""
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

class PromptTraceAPI:
    def __init__(self, db_path: str = "promptrace.db"):
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.db = DatabaseManager(db_path)
        self._setup_routes()
        
    def _setup_routes(self):
        @self.app.route("/experiments", methods=["GET"])
        def get_experiments():
            try:
                with self.db.get_connection() as conn:
                    # Use dictionary cursor
                    conn.row_factory = self.db.dict_factory
                    cursor = conn.cursor()
                    
                    # Get experiments with summary statistics
                    cursor.execute("""
                        SELECT 
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
                            eval,
                            created_at                      
                        FROM experiment 
                    """)
                    
                    experiments = cursor.fetchall()                    
                    
                    return jsonify({                        
                            "experiments": experiments                       
                    })
                    
            except sqlite3.Error as e:
                logger.error(f"Database error: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": "Database error occurred",
                    "error": str(e)
                }), 500
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return jsonify({
                    "status": "error",
                    "message": "An unexpected error occurred",
                    "error": str(e)
                }), 500
    
    def run(self, host: str = "127.0.0.1", port: int = 5000):
        self.app.run(host=host, port=port)

