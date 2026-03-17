"""
View component of MVC framework.
Handles HTML template rendering and presentation.
"""

import os
from typing import Dict, Any, Optional
from string import Template


class View:
    """Generic view for rendering HTML templates."""
    
    def __init__(self, templates_dir: str = "templates"):
        """
        Initialize the view with a templates directory.
        
        Args:
            templates_dir: Directory containing HTML template files
        """
        self.templates_dir = templates_dir
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
    
    def render_template(self, template_name: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Render an HTML template with the given context using standard Python template syntax.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to substitute in template
            
        Returns:
            Rendered HTML as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            TemplateError: If template syntax is invalid
        """
        if context is None:
            context = {}
        
        template_path = os.path.join(self.templates_dir, template_name)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Process double braces in CSS (convert {{ }} to { } for CSS, but keep {variable} for template vars)
            template_content = self._process_css_braces(template_content)
            
            # Apply standard Python string formatting only (no custom syntax)
            return template_content.format(**context)
        except Exception as e:
            # Add debugging info
            print(f"Debug: Context keys: {list(context.keys())}")
            print(f"Debug: Template content length: {len(template_content) if 'template_content' in locals() else 'N/A'}")
            raise TemplateError(f"Error rendering template {template_name}: {e}")
    
    def _process_css_braces(self, content: str) -> str:
        """
        Process double braces in CSS to avoid conflicts with template variables.
        Converts {{ }} to { } in CSS blocks while preserving {variable} syntax.
        
        Args:
            content: Template content
            
        Returns:
            Processed content with CSS braces converted
        """
        import re
        
        # Find CSS blocks (content between <style> and </style>)
        css_pattern = r'<style[^>]*>(.*?)</style>'
        
        def replace_css_braces(css_match):
            css_content = css_match.group(1)
            # Replace {{ with { and }} with } in CSS content
            css_content = css_content.replace('{{', '{').replace('}}', '}')
            # Escape braces for format() by doubling them
            css_content = css_content.replace('{', '{{').replace('}', '}}')
            return f'<style>{css_content}</style>'
        
        # Apply replacement to all CSS blocks
        processed_content = re.sub(css_pattern, replace_css_braces, content, flags=re.DOTALL)
        
        return processed_content
    
    def render_html(self, html_content: str, content_type: str = "text/html") -> bytes:
        """
        Convert HTML content to bytes for HTTP response.
        
        Args:
            html_content: HTML content as string
            content_type: MIME type for the content
            
        Returns:
            HTML content as bytes with HTTP headers
        """
        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: {content_type}; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += html_content
        
        return response.encode('utf-8')
    
    def render_json(self, data: Any) -> bytes:
        """
        Convert data to JSON response.
        
        Args:
            data: Data to serialize as JSON
            
        Returns:
            JSON response as bytes with HTTP headers
        """
        import json
        json_content = json.dumps(data, indent=2)
        
        response = f"HTTP/1.1 200 OK\r\n"
        response += "Content-Type: application/json; charset=utf-8\r\n"
        response += f"Content-Length: {len(json_content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += json_content
        
        return response.encode('utf-8')
    
    def redirect(self, location: str) -> bytes:
        """
        Create HTTP redirect response.
        
        Args:
            location: URL to redirect to
            
        Returns:
            HTTP redirect response as bytes
        """
        response = f"HTTP/1.1 302 Found\r\n"
        response += f"Location: {location}\r\n"
        response += "\r\n"
        
        return response.encode('utf-8')
    
    def error_response(self, status_code: int, message: str) -> bytes:
        """
        Create HTTP error response.
        
        Args:
            status_code: HTTP status code
            message: Error message
            
        Returns:
            HTTP error response as bytes
        """
        status_messages = {
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error"
        }
        
        status_text = status_messages.get(status_code, "Error")
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error {status_code}</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                h1 {{ color: #d32f2f; }}
            </style>
        </head>
        <body>
            <h1>Error {status_code}: {status_text}</h1>
            <p>{message}</p>
        </body>
        </html>
        """
        
        response = f"HTTP/1.1 {status_code} {status_text}\r\n"
        response += f"Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += html_content
        
        return response.encode('utf-8')


class TemplateError(Exception):
    """Exception raised for template-related errors."""
    pass
