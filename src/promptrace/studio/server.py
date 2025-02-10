import threading
from http.server import HTTPServer
from typing import Optional

from promptrace.config import TracerConfig
from promptrace.studio.api import StudioApi
from promptrace.studio.web import StudioWebHandler
          
class StudioServer:
    def __init__(self,  tracer_config: TracerConfig, port: int):
        self.tracer_config = tracer_config
        self.port = port

        self.web_server: Optional[HTTPServer] = None
        self.api_server: Optional[StudioApi] = None
        self.api_thread: Optional[threading.Thread] = None
        
    def start_api_server(self):
        self.api_server = StudioApi(self.tracer_config.db_server)
        self.api_thread = threading.Thread(
            target=self.api_server.run,
            args=("localhost", self.port + 1),
            daemon=True
        )
        self.api_thread.start()
    
    def start_web_server(self, port: int):
        self.web_server = HTTPServer(
            ("localhost", port),
            StudioWebHandler
        )

        try:
            self.web_server.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown all servers"""
        if self.web_server:
            self.web_server.shutdown()
            
        if self.api_thread and self.api_thread.is_alive():
            self.api_thread.join(timeout=5)
    
    def start(self, db_path: str, base_port: int = 8000):
        try:
            # Start API server first
            self.start_api_server(db_path, base_port + 1)
            
            # Start web server in main thread
            self.start_web_server(base_port)
            
        except Exception as e:
            self.shutdown()
            raise 