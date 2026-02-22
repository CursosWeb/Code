
"""Prompt usado:

Escribe codigo para descargarte el listado de issues del proyecto
"cursoprogram/bifurca-repositorio" de una instancia de GitLab que está
accesible en https://gitlab.eif.urjc.es.
Incluye este prompt como comentario al principio del programa.
Hazlo con urllib, no con requests.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
from typing import List, Dict, Any

class GitLabIssueDownloader:
    def __init__(self, gitlab_url: str, token: str = None):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.token = token
    
    def get_project_issues(self, project_path: str) -> List[Dict[str, Any]]:
        """
        Download all issues from a GitLab project
        
        Args:
            project_path: Project path in format "group/project"
            
        Returns:
            List of issue dictionaries
        """
        encoded_path = urllib.parse.quote(project_path, safe='')
        base_url = f"{self.gitlab_url}/api/v4/projects/{encoded_path}/issues"
        
        all_issues = []
        page = 1
        
        while True:
            params = {
                'page': str(page),
                'per_page': '100',
                'state': 'all'  # Get both open and closed issues
            }
            
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            try:
                req = urllib.request.Request(url)
                if self.token:
                    req.add_header('PRIVATE-TOKEN', self.token)
                
                with urllib.request.urlopen(req) as response:
                    data = response.read().decode('utf-8')
                    issues = json.loads(data)
                    
                if not issues:
                    break
                    
                all_issues.extend(issues)
                print(f"Downloaded {len(issues)} issues from page {page}")
                page += 1
                
            except urllib.error.URLError as e:
                print(f"Error fetching issues: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                break
        
        return all_issues
    
    def save_issues_to_json(self, issues: List[Dict[str, Any]], filename: str):
        """Save issues to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(issues, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(issues)} issues to {filename}")

def main():
    # GitLab instance configuration
    gitlab_url = "https://gitlab.eif.urjc.es"
    project_path = "cursoprogram/bifurca-repositorio"
    
    # Optional: Add your GitLab access token here for higher rate limits
    # You can create a token at: https://gitlab.eif.urjc.es/-/profile/personal_access_tokens
    access_token = None  # Set to your token if needed
    
    downloader = GitLabIssueDownloader(gitlab_url, access_token)
    
    print(f"Downloading issues from {gitlab_url}")
    print(f"Project: {project_path}")
    print("-" * 50)
    
    try:
        issues = downloader.get_project_issues(project_path)
        
        if issues:
            print(f"\nSuccessfully downloaded {len(issues)} issues")
            
            # Save to JSON file
            output_file = "gitlab_issues.json"
            downloader.save_issues_to_json(issues, output_file)
            
            # Print summary
            open_issues = len([i for i in issues if i['state'] == 'opened'])
            closed_issues = len([i for i in issues if i['state'] == 'closed'])
            
            print(f"\nIssue Summary:")
            print(f"- Open issues: {open_issues}")
            print(f"- Closed issues: {closed_issues}")
            print(f"- Total issues: {len(issues)}")
            
            # Show first few issues as example
            if issues:
                print(f"\nFirst 3 issues:")
                for i, issue in enumerate(issues[:3]):
                    print(f"{i+1}. #{issue['iid']}: {issue['title']} ({issue['state']})")
        else:
            print("No issues found or unable to access the project")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()