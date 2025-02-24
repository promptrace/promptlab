from promptrace.experiment import Experiment
from promptrace.model.model_factory import ModelFactory
from promptrace.tracer.tracer_factory import TracerFactory
from promptrace.prompt import Prompt
from promptrace.config import ConfigValidator
from promptrace.studio.server import StudioServer
from promptrace.deployment import Deployment

class PrompTrace:
    """
    The PrompTrace class is responsible for managing the execution of experiments
    and starting the studio server. It validates configurations, runs experiments,
    and traces the results.
    """

    def __init__(self, tracer_config: dict):
        """
        Initialize the PrompTrace instance with the given tracer configuration.

        Args:
            tracer_config (dict): Configuration for the tracer. Pass a json object with the following structure:

            {
                "type": "<tracer_type>",
                "db_server": "<db_server>"
            }
        """
        self.tracer_config = ConfigValidator.validate_tracer_config(tracer_config)
    
    def run(self, experiment_config: dict):
        """
        Run an experiment with the given experiment configuration.

        Args:
            experiment_config (dict): Configuration for the experiment. Pass a json object with the following structure:
            
            {
                "model" : {
                        "type": "<model_type>",
                        "api_key": "<api_key>", 
                        "api_version": "<api_version>", 
                        "endpoint": "<endpoint>",
                        "deployment": "<deployment>"
                },
                "prompt_template": "<prompt_template_path>",
                "dataset": "<dataset_path>",
                "variable_map": {
                    "context": "context",
                    "question": "question"
                },
                "evaluation": ['<metric_name>']
            }
        """
        self.experiment_config = ConfigValidator.validate_experiment_config(experiment_config)

        model = ModelFactory.get_model(self.experiment_config.model)
        prompt = Prompt(prompt_template=self.experiment_config.prompt_template)
        experiment = Experiment(self.experiment_config)

        experiment_summary = experiment.start(model, prompt)

        tracer = TracerFactory.get_tracer(self.tracer_config)
        tracer.trace(experiment_summary)

    def start_studio(self, port: int):
        server = StudioServer(self.tracer_config, port)
        server.start()

    def deploy(self, experiment_id: str, deployment_dir: str):
        Deployment.deploy(experiment_id, deployment_dir, self.tracer_config.db_server)