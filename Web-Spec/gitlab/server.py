#!/usr/bin/env python3

"""Prompt usado:

Crea un programa, server.py, que muestre en su página principal
un formulario, en el que se puede poner el nombre de un repositorio.
Cuando se ponga, mostrará el listado de los issues de ese repositorio.
Usa la clase definida en @issues.py para acceder a la lista de
issues de GitLab de EIF.
Para todas las páginas HTML, pon las templates en un fichero
templates.py, para simplificar el código.
En las templates sustituye { y } por dobles, para que funcionen bien
las plantillas cuando no se quieren sustituir las variables.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import html
from templates import FORM_TEMPLATE, ERROR_TEMPLATE, ISSUES_TEMPLATE, ISSUE_ITEM_TEMPLATE
from issues import GitLabIssueDownloader

class GitLabIssueHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.gitlab_url = "https://gitlab.eif.urjc.es"
        self.downloader = GitLabIssueDownloader(self.gitlab_url)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_form()
        elif parsed_path.path == '/issues':
            query_params = parse_qs(parsed_path.query)
            repo_name = query_params.get('repo', [None])[0]
            
            if repo_name:
                self.serve_issues(repo_name)
            else:
                self.serve_form(error="Por favor, introduce un nombre de repositorio")
        else:
            self.send_error(404, "Página no encontrada")
    
    def serve_form(self, error=None):
        """Serve the main form page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        error_message = f'<div class="error">{error}</div>' if error else ''
        html_content = FORM_TEMPLATE.format(error_message=error_message)
        
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_issues(self, repo_name):
        """Serve the issues page"""
        issues = self.downloader.get_project_issues(repo_name)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        if issues is None:
            error_html = ERROR_TEMPLATE.format(repo_name=html.escape(repo_name))
            self.wfile.write(error_html.encode('utf-8'))
            return
        
        # Limit to 50 issues for display
        issues = issues[:50]
        
        # Count issues by state
        open_issues = len([i for i in issues if i['state'] == 'opened'])
        closed_issues = len([i for i in issues if i['state'] == 'closed'])
        
        # Generate issues HTML
        issues_html = ""
        for issue in issues:
            state_icon = "🟢" if issue['state'] == 'opened' else "🔴"
            state_text = "Abierto" if issue['state'] == 'opened' else "Cerrado"
            title = html.escape(issue.get('title', 'Sin título'))
            description = html.escape(issue.get('description', ''))[:200]
            if len(issue.get('description', '')) > 200:
                description += "..."
            
            issues_html += ISSUE_ITEM_TEMPLATE.format(
                issue_number=issue['iid'],
                state=issue['state'],
                state_icon=state_icon,
                state_text=state_text,
                title=title,
                description=description,
                web_url=issue.get('web_url', '#')
            )
        
        if not issues_html:
            issues_html = '<div class="no-issues">No se encontraron issues en este repositorio.</div>'
        
        html_content = ISSUES_TEMPLATE.format(
            repo_name=html.escape(repo_name),
            total_issues=len(issues),
            open_issues=open_issues,
            closed_issues=closed_issues,
            issues_html=issues_html
        )
        
        self.wfile.write(html_content.encode('utf-8'))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, GitLabIssueHandler)
    print(f"🚀 Servidor iniciado en http://localhost:{port}")
    print("Presiona Ctrl+C para detener el servidor")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
