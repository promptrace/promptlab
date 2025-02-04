import http
from pathlib import Path
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
from typing import Optional
import os

import pkg_resources
from promptrace.serving.api import PromptTraceAPI

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
            
class _Server:
    def __init__(self):
        
        self.web_server: Optional[HTTPServer] = None
        self.api_server: Optional[PromptTraceAPI] = None
        self.api_thread: Optional[threading.Thread] = None
        
    def start_api_server(self, db_path: str, port: int):
        db_path = db_path.replace("\t", "\\t")
        db_path = os.path.join(db_path, 'promptrace.db')

        self.api_server = PromptTraceAPI(str(db_path))
        self.api_thread = threading.Thread(
            target=self.api_server.run,
            args=("localhost", port),
            daemon=True
        )
        self.api_thread.start()
    
    def start_web_server(self, port: int):
        self.web_server = HTTPServer(
            ("localhost", port),
            CustomHandler
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