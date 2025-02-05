import http
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

import pkg_resources
from promptrace.experiment import Experiment
from promptrace.model import Model
from promptrace.prompt import Prompt
from promptrace.config import ExperimentConfig, TracerConfig, ConfigValidator
from promptrace.serving.server import _Server
from promptrace.tracers.tracer_factory import TracerFactory
import os

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = pkg_resources.resource_filename("web", "index.html")
            with open(self.path, "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())
        else:
            super().do_GET()

class PrompTrace:
    def __init__(self, tracer: dict):
        self.tracer = ConfigValidator.validate_tracer_config(tracer)
    
    def run(self, _experiment_config: dict):
        self.experiment_config = ConfigValidator.validate_experiment_config(_experiment_config)
        
        model = Model(model_config=self.experiment_config.model)
        prompt = Prompt(prompt_template=self.experiment_config.prompt_template)

        experiment = Experiment(self.experiment_config)
        run_result = experiment.run(model, prompt)

        tracer = TracerFactory.get_tracer(self.tracer.type, self.tracer.target)
        tracer.trace(run_result)

    def start_web_server(self, db_dir: str, port: int = 8000):
        server = _Server()
        server.start(db_dir, port)