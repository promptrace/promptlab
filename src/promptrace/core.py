from promptrace.asset.asset import Asset
from promptrace.db.sql_query import SQLQuery
from promptrace.experiment import Experiment
from promptrace.tracer.tracer_factory import TracerFactory
from promptrace.config import ConfigValidator
from promptrace.studio.server import StudioServer
from promptrace.deployment import Deployment
from promptrace.db.db import get_db_connection

class PrompTrace:

    def __init__(self, tracer_config: dict):
        tracer_config = ConfigValidator.validate_tracer_config(tracer_config)        
        self.connection = get_db_connection(tracer_config)
        self.tracer_config = tracer_config

        self.connection.execute(SQLQuery.CREATE_ASSETS_TABLE_QUERY)
        self.connection.execute(SQLQuery.CREATE_EXPERIMENTS_TABLE_QUERY)
        self.connection.execute(SQLQuery.CREATE_EXPERIMENT_RESULT_TABLE_QUERY)
        self.connection.commit()

        self.tracer = TracerFactory.get_tracer(tracer_config.type, self.connection)
        self.asset = Asset(self.connection)
        self.experiment = Experiment(self.connection)

    def start_studio(self, port: int):
        server = StudioServer(self.tracer_config, port)
        server.start()

    def deploy(self, experiment_id: str, deployment_dir: str):
        Deployment.deploy(experiment_id, deployment_dir, self.tracer_config.db_server)