#!/usr/bin/env python3

"""Prompt usado:

Ahora, crea el programa gitlab.py, con una clase que tenga una función para 
listar los issues de un proyecto en el GitLab de la EIF, y otra para crear 
un nuevo issue en ese mismo repo. El programa principal instanciará esa clase, 
y aceptará argumentos para listar issues, y para crear uno nuevo.
Lee un fichero .env para leer el token de GitLab de él.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import argparse
import sys
import os
from typing import List, Dict, Any, Optional

class GitLabManager:
    def __init__(self, gitlab_url: str = "https://gitlab.eif.urjc.es", token: Optional[str] = None):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.token = token
    
    def _make_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request to GitLab API"""
        try:
            req = urllib.request.Request(url)
            
            if self.token:
                req.add_header('PRIVATE-TOKEN', self.token)
            
            if method == 'POST' and data:
                req.add_header('Content-Type', 'application/json')
                json_data = json.dumps(data).encode('utf-8')
                req.data = json_data
                req.get_method = lambda: 'POST'
            
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
                
        except urllib.error.URLError as e:
            print(f"Error de red: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al procesar JSON: {e}")
            return None
    
    def list_issues(self, project_path: str, state: str = 'all') -> List[Dict[str, Any]]:
        """
        List issues from a GitLab project
        
        Args:
            project_path: Project path in format "group/project"
            state: Issue state ('opened', 'closed', 'all')
            
        Returns:
            List of issue dictionaries
        """
        encoded_path = urllib.parse.quote(project_path, safe='')
        base_url = f"{self.gitlab_url}/api/v4/projects/{encoded_path}/issues"
        
        all_issues = []
        page = 1
        
        print(f"Listando issues del proyecto: {project_path}")
        print("-" * 50)
        
        while True:
            params = {
                'page': str(page),
                'per_page': '100',
                'state': state
            }
            
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            issues_data = self._make_request(url)
            
            if not issues_data:
                break
            
            if not isinstance(issues_data, list):
                print("Error: La respuesta no es una lista de issues")
                break
            
            if not issues_data:
                break
                
            all_issues.extend(issues_data)
            print(f"Descargados {len(issues_data)} issues (página {page})")
            page += 1
        
        return all_issues
    
    def create_issue(self, project_path: str, title: str, description: str = "") -> Optional[Dict[str, Any]]:
        """
        Create a new issue in a GitLab project
        
        Args:
            project_path: Project path in format "group/project"
            title: Issue title
            description: Issue description
            
        Returns:
            Created issue dictionary or None if failed
        """
        if not self.token:
            print("Error: Se requiere un token de acceso para crear issues")
            print("Crea un token en: https://gitlab.eif.urjc.es/-/user_settings/personal_access_tokens")
            return None
        
        encoded_path = urllib.parse.quote(project_path, safe='')
        url = f"{self.gitlab_url}/api/v4/projects/{encoded_path}/issues"
        
        issue_data = {
            'title': title,
            'description': description
        }
        
        print(f"Creando issue en {project_path}: {title}")
        print("-" * 50)
        
        result = self._make_request(url, method='POST', data=issue_data)
        
        if result:
            print(f"✅ Issue creado exitosamente:")
            print(f"   Título: {result.get('title', 'N/A')}")
            print(f"   ID: #{result.get('iid', 'N/A')}")
            print(f"   URL: {result.get('web_url', 'N/A')}")
            return result
        else:
            print("❌ Error al crear el issue")
            return None
    
    def print_issues_summary(self, issues: List[Dict[str, Any]]):
        """Print a summary of issues"""
        if not issues:
            print("No se encontraron issues")
            return
        
        open_issues = len([i for i in issues if i['state'] == 'opened'])
        closed_issues = len([i for i in issues if i['state'] == 'closed'])
        
        print(f"\n📊 Resumen:")
        print(f"   Total: {len(issues)}")
        print(f"   🟢 Abiertos: {open_issues}")
        print(f"   🔴 Cerrados: {closed_issues}")
        print()
        
        print("📋 Issues recientes:")
        for i, issue in enumerate(issues[:10]):
            state_icon = "🟢" if issue['state'] == 'opened' else "🔴"
            state_text = "Abierto" if issue['state'] == 'opened' else "Cerrado"
            title = issue.get('title', 'Sin título')
            print(f"   {i+1}. #{issue['iid']} {state_icon} {title} ({state_text})")
        
        if len(issues) > 10:
            print(f"   ... y {len(issues) - 10} más")

def load_token_from_env() -> Optional[str]:
    """Load GitLab token from .env file"""
    env_file = '.env'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GITLAB_TOKEN='):
                        return line.split('=', 1)[1].strip().strip('"\'')
        except Exception as e:
            print(f"Error leyendo .env: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description='Gestor de issues de GitLab EIF')
    parser.add_argument('--token', help='Token de acceso personal de GitLab')
    parser.add_argument('--project', default='cursoprogram/bifurca-repositorio', 
                       help='Proyecto GitLab (default: cursoprogram/bifurca-repositorio)')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando para listar issues
    list_parser = subparsers.add_parser('list', help='Listar issues del proyecto')
    list_parser.add_argument('--state', choices=['opened', 'closed', 'all'], 
                          default='all', help='Estado de los issues (default: all)')
    
    # Comando para crear issue
    create_parser = subparsers.add_parser('create', help='Crear nuevo issue')
    create_parser.add_argument('title', help='Título del issue')
    create_parser.add_argument('--description', help='Descripción del issue')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Determinar token: prioridad --token > .env > None
    token = args.token or load_token_from_env()
    
    # Crear instancia del gestor
    manager = GitLabManager(token=token)
    
    if args.command == 'list':
        issues = manager.list_issues(args.project, args.state)
        manager.print_issues_summary(issues)
        
    elif args.command == 'create':
        issue = manager.create_issue(args.project, args.title, args.description)
        if issue:
            print(f"\n✨ Issue #{issue['iid']} creado exitosamente")
        else:
            print("\n💥 No se pudo crear el issue")
            sys.exit(1)

if __name__ == "__main__":
    main()
