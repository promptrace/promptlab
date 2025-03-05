from flask import Flask, jsonify
from flask_cors import CORS

from promptrace.db.sql import SQLQuery
from promptrace.types import TracerConfig
from promptrace.utils import Utils

class StudioApi:
 
    def __init__(self, tracer_config: TracerConfig):

        self.tracer_config = tracer_config
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})

        self._setup_routes()
        
    def _setup_routes(self):

        @self.app.route("/experiments", methods=["GET"])
        def get_experiments():
            try:               
                experiments = self.tracer_config.db_client.fetch_data(SQLQuery.SELECT_EXPERIMENTS_QUERY)
                
                # Process experiments and remove asset_binary
                processed_experiments = []
                for experiment in experiments:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(experiment["asset_binary"])
                    # Create new dict without asset_binary
                    experiment_data = {k: v for k, v in experiment.items() if k != 'asset_binary'}
                    experiment_data["system_prompt_template"] = system_prompt
                    experiment_data["user_prompt_template"] = user_prompt
                    processed_experiments.append(experiment_data)

                return jsonify({                        
                        "experiments": processed_experiments                       
                })
                
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": "An unexpected error occurred",
                    "error": str(e)
                }), 500
    
    def run(self, host: str = "127.0.0.1", port: int = 5000):
        self.app.run(host=host, port=port)

