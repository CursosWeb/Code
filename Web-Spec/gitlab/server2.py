#!/usr/bin/env python3

"""Prompt usado:

Crea un servidor HTTP, server2.py, que muestre, si se solicita su 
recurso principal, un formulario para elegir un repositorio. Una vez 
recibido el formulario elegido, el servidor enviará una redirección a 
un recurso que se llame ingual que el repositorio elegido. Además, si se 
solicita un recurso con nombre de repositorio, devolverá el listado de 
issues del repositorio, y un formulario donde podrá ponerse un nuevo 
issue (mediante POST sobre ese mismo repositorio). Para listar y poner 
issues, usa la clase GitLabManager de @gitlab.py
"""

import urllib.request
import urllib.parse
import urllib.error
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import html
import os
from gitlab import GitLabManager, load_token_from_env
from templates2 import MAIN_TEMPLATE, REPO_TEMPLATE, ISSUE_ITEM_TEMPLATE

class GitLabRepoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.gitlab_manager = GitLabManager(token=load_token_from_env())
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        
        if path == '':
            # Página principal con formulario
            query_params = parse_qs(parsed_path.query)
            repo_name = query_params.get('repo', [None])[0]
            
            if repo_name:
                # Redirigir al recurso del repositorio
                self.send_response(302)
                self.send_header('Location', f'/{repo_name}')
                self.end_headers()
            else:
                # Mostrar formulario principal
                self.serve_main_form()
        else:
            # Mostrar repositorio específico
            self.serve_repository(path)
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        
        if path:
            # Crear nuevo issue en el repositorio
            self.create_issue(path)
    
    def serve_main_form(self):
        """Serve the main form page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(MAIN_TEMPLATE.encode('utf-8'))
    
    def serve_repository(self, repo_name: str):
        """Serve repository issues page"""
        issues = self.gitlab_manager.list_issues(repo_name)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        if issues is None:
            error_html = f"""
            <div class="error">
                <h2>❌ Error al obtener los issues</h2>
                <p>No se pudieron obtener los issues del repositorio <strong>{html.escape(repo_name)}</strong></p>
                <p>Verifica que el nombre del repositorio sea correcto y que el proyecto sea público.</p>
            </div>
            """
            html_content = REPO_TEMPLATE.format(
                repo_name=html.escape(repo_name),
                total_issues=0,
                open_issues=0,
                closed_issues=0,
                error_message=error_html,
                issues_html='<div class="no-issues">No se encontraron issues en este repositorio.</div>'
            )
            self.wfile.write(html_content.encode('utf-8'))
            return
        
        # Limitar a 50 issues para visualización
        issues = issues[:50]
        
        # Contar issues por estado
        open_issues = len([i for i in issues if i['state'] == 'opened'])
        closed_issues = len([i for i in issues if i['state'] == 'closed'])
        
        # Generar HTML de issues
        issues_html = ""
        for issue in issues:
            state_icon = "🟢" if issue['state'] == 'opened' else "🔴"
            state_text = "Abierto" if issue['state'] == 'opened' else "Cerrado"
            title = html.escape(issue.get('title', 'Sin título'))
            description = issue.get('description', '')
            if description is None:
                description = ''
            else:
                description = html.escape(description)
                if len(description) > 200:
                    description += description[:200] + "..."
            
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
        
        html_content = REPO_TEMPLATE.format(
            repo_name=html.escape(repo_name),
            total_issues=len(issues),
            open_issues=open_issues,
            closed_issues=closed_issues,
            error_message='',
            issues_html=issues_html
        )
        
        self.wfile.write(html_content.encode('utf-8'))
    
    def create_issue(self, repo_name: str):
        """Create a new issue in the repository"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parsear datos del formulario
        params = parse_qs(post_data)
        title = params.get('title', [''])[0]
        description = params.get('description', [''])[0]
        
        if not title:
            # Redirigir con error
            self.send_response(302)
            self.send_header('Location', f'/{repo_name}?error=title_required')
            self.end_headers()
            return
        
        # Crear issue usando GitLabManager
        issue = self.gitlab_manager.create_issue(repo_name, title, description)
        
        if issue:
            # Redirigir al repositorio tras crear exitosamente
            self.send_response(302)
            self.send_header('Location', f'/{repo_name}')
            self.end_headers()
        else:
            # Redirigir con error
            self.send_response(302)
            self.send_header('Location', f'/{repo_name}?error=create_failed')
            self.end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, GitLabRepoHandler)
    print(f"🚀 Servidor iniciado en http://localhost:{port}")
    print("Presiona Ctrl+C para detener el servidor")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
