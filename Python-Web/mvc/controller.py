"""
Controller component of MVC framework.
Handles HTTP server and request routing using socketserver directly.
"""

import socketserver
import socket
import urllib.parse
from typing import Dict, Callable, Any, Optional, Tuple
from model import Model
from view import View


class HTTPRequestHandler(socketserver.BaseRequestHandler):
    """Custom HTTP request handler using socketserver directly."""
    
    def handle(self):
        """Handle incoming HTTP requests."""
        try:
            # Receive HTTP request
            request_data = self.request.recv(4096).decode('utf-8')
            if not request_data:
                return
            
            # Parse HTTP request
            lines = request_data.split('\r\n')
            if not lines:
                return
            
            # Parse request line
            request_line = lines[0].strip()
            parts = request_line.split(' ')
            if len(parts) < 2:
                return
            
            method = parts[0].upper()
            path = parts[1]
            
            # Parse headers
            headers = {}
            body = ""
            body_started = False
            
            for line in lines[1:]:
                if line.strip() == '':
                    body_started = True
                    continue
                
                if not body_started:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip().lower()] = value.strip()
                else:
                    body += line + '\r\n'
            
            # Remove trailing \r\n from body
            body = body.rstrip('\r\n')
            
            # Create request context
            request_context = {
                'method': method,
                'path': path.split('?')[0],
                'full_path': path,
                'headers': headers,
                'body': body
            }
            
            # Parse query parameters
            if '?' in path:
                query_string = path.split('?', 1)[1]
                request_context['query_params'] = urllib.parse.parse_qs(query_string, keep_blank_values=True)
            else:
                request_context['query_params'] = {}
            
            # Parse POST data
            if method == 'POST' and body:
                request_context['post_data'] = urllib.parse.parse_qs(body, keep_blank_values=True)
            else:
                request_context['post_data'] = {}
            
            # Get MVC server instance
            mvc_server = self.server.mvc_server
            
            # Handle the request
            response = mvc_server.handle_request(request_context)
            
            # Send response
            self.request.send(response)
            
        except Exception as e:
            # Send error response
            error_response = f"HTTP/1.1 500 Internal Server Error\r\n"
            error_response += "Content-Type: text/plain\r\n"
            error_response += f"Content-Length: {len(str(e))}\r\n"
            error_response += "\r\n"
            error_response += str(e)
            try:
                self.request.send(error_response.encode('utf-8'))
            except:
                pass


class MVCServer:
    """Main MVC server that coordinates model, view, and routing."""
    
    def __init__(self, host: str = "localhost", port: int = 8000, 
                 storage_file: str = "app_state", templates_dir: str = "templates"):
        """
        Initialize the MVC server.
        
        Args:
            host: Server hostname
            port: Server port
            storage_file: File for model persistence
            templates_dir: Directory for view templates
        """
        self.host = host
        self.port = port
        self.model = Model(storage_file)
        self.view = View(templates_dir)
        self.routes: Dict[Tuple[str, str], Callable] = {}
        self.http_server = None
    
    def add_route(self, method: str, path_pattern: str, handler: Callable):
        """
        Add a route for HTTP requests.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path_pattern: URL path pattern (supports simple wildcards)
            handler: Function to handle the request
        """
        route_key = (method.upper(), path_pattern)
        self.routes[route_key] = handler
    
    def match_route(self, method: str, path: str) -> Optional[Tuple[Callable, Dict[str, str]]]:
        """
        Find matching route for request.
        
        Args:
            method: HTTP method
            path: Request path
            
        Returns:
            Tuple of (handler, path_params) or None if no match
        """
        for (route_method, route_pattern), handler in self.routes.items():
            if route_method != method.upper():
                continue
            
            # Simple pattern matching (support for wildcards)
            if route_pattern == path:
                return handler, {}
            elif '*' in route_pattern or ':' in route_pattern:
                # Convert pattern to regex for wildcard matching
                pattern_parts = route_pattern.split('/')
                path_parts = path.split('/')
                
                if len(pattern_parts) != len(path_parts):
                    continue
                
                params = {}
                match = True
                for pattern_part, path_part in zip(pattern_parts, path_parts):
                    if pattern_part == '*':
                        continue
                    elif pattern_part.startswith(':') and pattern_part[1:]:
                        params[pattern_part[1:]] = path_part
                    elif pattern_part != path_part:
                        match = False
                        break
                
                if match:
                    return handler, params
        
        return None, {}
    
    def handle_request(self, request_context: Dict[str, Any]) -> bytes:
        """
        Handle incoming HTTP request.
        
        Args:
            request_context: Dictionary containing request information
            
        Returns:
            HTTP response as bytes
        """
        try:
            method = request_context['method']
            path = request_context['path']
            
            route_handler, path_params = self.match_route(method, path)
            
            if route_handler:
                # Add path params to request context
                request_context['path_params'] = path_params
                
                # Call the route handler
                response = route_handler(self.model, self.view, request_context)
                
                # Ensure response is bytes
                if isinstance(response, str):
                    return self.view.render_html(response)
                elif isinstance(response, bytes):
                    return response
                else:
                    # Assume it's HTML string
                    return self.view.render_html(str(response))
            else:
                # No route found - 404
                return self.view.error_response(404, f"Route not found: {method} {path}")
        
        except Exception as e:
            # Internal server error
            return self.view.error_response(500, f"Internal server error: {str(e)}")
    
    def run(self):
        """Start the HTTP server."""
        # Create a custom server class that includes reference to MVC server
        class CustomTCPServer(socketserver.TCPServer):
            def __init__(self, server_address, RequestHandlerClass, mvc_server):
                self.mvc_server = mvc_server
                super().__init__(server_address, RequestHandlerClass)
        
        self.http_server = CustomTCPServer((self.host, self.port), HTTPRequestHandler, self)
        print(f"MVC Server running on http://{self.host}:{self.port}")
        
        try:
            self.http_server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        finally:
            if self.http_server:
                self.http_server.server_close()
    
    def stop(self):
        """Stop the HTTP server."""
        if self.http_server:
            self.http_server.shutdown()
            self.http_server.server_close()
