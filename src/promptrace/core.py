from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from promptrace.experiment import Experiment
from promptrace.model import Model
from promptrace.prompt import Prompt
from promptrace.config import ExperimentConfig, TracerConfig
from promptrace.tracers.tracer_factory import TracerFactory
import os
from typing import List, Dict, Any

from web.api import PromptTraceAPI
    
class PrompTrace:
    def __init__(self, tracer: dict):
        self.tracer = self.validate_tracer_config(tracer)
    
    def validate_tracer_config(self, tracer: dict) -> TracerConfig:
        try:
            return TracerConfig.model_validate(tracer)
        except Exception as e:
            raise ValueError(f"Invalid tracer configuration: {str(e)}")

    def validate_experiment_config(self, experiment_config: dict) -> ExperimentConfig:
        try:
            return ExperimentConfig.model_validate(experiment_config)
        except Exception as e:
            raise ValueError(f"Invalid experiment configuration: {str(e)}")

    def run(self, _experiment_config: dict):
        self.experiment_config = self.validate_experiment_config(_experiment_config)
        
        model = Model(model_config=self.experiment_config.model)
        prompt = Prompt(prompt_template=self.experiment_config.prompt_template)

        experiment = Experiment(self.experiment_config)
        run_result = experiment.run(model, prompt)

        tracer = TracerFactory.get_tracer(self.tracer.type, self.tracer.target)
        tracer.trace(run_result, self.experiment_config.evaluation)
        
    def start_web_server(self, html_path: str, port: int = 8000):
        """Start the web server and API"""
        html_path = html_path.replace("\t", "\\t")
        os.chdir(html_path)
        
        # Initialize API
        api = PromptTraceAPI(self.tracer.target+'/promptrace.db')
        
        # Start API in a separate thread
        import threading
        api_thread = threading.Thread(target=api.run, args=("localhost", port+1))
        api_thread.daemon = True
        api_thread.start()
        
        # Start HTTP server for static files
        handler = SimpleHTTPRequestHandler
        httpd = HTTPServer(("localhost", port), handler)
        print(f"Serving HTTP on localhost port {port} (http://localhost:{port}/) ...")
        print(f"API running on port {port+1}")
        httpd.serve_forever()