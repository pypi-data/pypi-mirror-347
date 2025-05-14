import http.server
import socketserver
import json
import webbrowser
import socket
import threading
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional
from string import Template

class CallbackServer:
    """
    A simple HTTP server for opening a browser page and waiting for user callback responses.
    
    This server is designed to present users with a web interface containing questions and options,
    and collect responses. The server runs locally on a specified or automatically discovered port,
    serves an HTML page with dynamic content, and listens for user responses via HTTP requests.
    
    Attributes:
        port (int): The port on which the server will listen. Default is 3333.
        server (Optional[socketserver.TCPServer]): The instance of the TCP server.
        session_id (str): A unique identifier for the server session.
        response_data (Optional[Dict[str, Any]]): Data received from the user after form submission.
        timeout_seconds (int): Duration to wait for user responses before timeout. Default is 300 seconds.
        initial_data (Optional[Dict[str, Dict[str, Any]]]): Initial data containing questions and options.
        server_thread (Optional[threading.Thread]): The thread running the server.
        html_template (Optional[str]): The HTML template for the web page served to the user.
    """
    def __init__(self, port: int = 3333):
        self.port = port
        self.server = None
        self.session_id = f"{int(time.time())}-{id(self)}"
        self.response_data = None
        self.timeout_seconds = 300  # Default 5 minutes timeout
        self.initial_data = None
        self.server_thread = None
        self.html_template = None
        
    def _find_available_port(self) -> int:
        """
        Find an available port
        """
        port = self.port
        for _ in range(100):  # Try 100 times
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("127.0.0.1", port))
                    return port
                except socket.error:
                    port += 1
        raise RuntimeError("Unable to find an available port")
    
    def _create_handler(self):
        """
        Create HTTP request handler
        """
        server_instance = self
        
        class CallbackHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(Path(__file__).parent / "static"), **kwargs)
            
            def log_message(self, format, *args):
                # Disable log output
                pass
            
            def do_GET(self):
                parsed_path = urllib.parse.urlparse(self.path)
                
                # Handle root path request
                if parsed_path.path == "/":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    
                    # Use HTML template
                    html_content = server_instance.html_template
                    self.wfile.write(html_content.encode())
                    return
                
                # Handle request for initial data
                if parsed_path.path == "/api/data":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    
                    response = {
                        "status": "success",
                        "data": server_instance.initial_data
                    }
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Handle static files
                try:
                    super().do_GET()
                except:
                    self.send_response(404)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"Not found")
            
            def do_POST(self):
                parsed_path = urllib.parse.urlparse(self.path)
                
                # Handle callback request
                if parsed_path.path == "/api/callback":
                    content_length = int(self.headers.get("Content-Length", 0))
                    post_data = self.rfile.read(content_length).decode("utf-8")
                    
                    try:
                        data = json.loads(post_data)
                        server_instance.response_data = data
                        
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "success"}).encode())
                        
                        # Shutdown the server
                        threading.Thread(target=server_instance.shutdown).start()
                    except Exception as e:
                        self.send_response(400)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
        
        return CallbackHandler
    
    def shutdown(self):
        """
        Shut down the server
        """
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(1)
    
    def _create_html_template(self, title: str, questions: Dict[str, Dict[str, Any]]) -> str:
        """
        Create HTML template containing multiple questions and options
        """
        # Get the path to the template file
        template_path = Path(__file__).parent / "templates" / "survey_template.html"
        
        # Read the template file
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        # Replace the title placeholder with the actual title
        # Using string.Template for simple variable substitution
        template = Template(template_content)
        return template.substitute(title=title)
    
    def prompt_user_with_options(self, title: str, questions: Dict[str, Dict[str, Any]], timeout_seconds: int = 300) -> Optional[Dict[str, Any]]:
        """
        Open a browser and wait for the user to select questions and options

        Args:
            title (str): Page title
            questions (Dict[str, Dict[str, Any]]): Dictionary of questions and options, format: {"Q1": {"question": "Question 1", "options": ["Option 1", "Option 2", ...]}}
            timeout_seconds (int): Timeout duration in seconds

        Returns:
            Optional[Dict[str, Any]]: User's selected questions and options data, or None if timeout occurs
        """
        self.timeout_seconds = timeout_seconds
        self.initial_data = questions
        self.html_template = self._create_html_template(title, questions)
        
        try:
            # Create static files directory
            static_dir = Path(__file__).parent / "static"
            static_dir.mkdir(exist_ok=True)
            
            # Find available port
            port = self._find_available_port()
            
            # Create server
            handler = self._create_handler()
            self.server = socketserver.TCPServer(("127.0.0.1", port), handler)
            
            # Start server in a new thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Open browser
            url = f"http://127.0.0.1:{port}"
            webbrowser.open(url)
            
            # Wait for response or timeout
            start_time = time.time()
            while self.response_data is None and time.time() - start_time < self.timeout_seconds:
                time.sleep(0.1)
            
            # Return result
            if self.response_data is not None:
                return self.response_data
            else:
                print("Timeout waiting for user response")
                return None
        finally:
            # Ensure server shutdown
            self.shutdown()
