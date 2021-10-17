#!/usr/bin/python3

#
# Simple program to get all the forks of a GitLab projects
#
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# April 2021
#
# GitLAb API doc:
# https://docs.gitlab.com/ee/api/projects.html#list-forks-of-a-project
# Command line example:
# curl --header "PRIVATE-TOKEN: <token>"
#   "https://gitlab.etsit.urjc.es/api/v4/projects/2799/forks"
#   | jq | grep http_url_to_repo

import json
import sys
import urllib.request

def get_forks(gitlab_instance, repo_id, api_token):
    """Get list of forks for a given GitLab repo id"""
    api_url = gitlab_instance + "/api/v4/projects/" + repo_id + "/forks"

    headers = {"PRIVATE-TOKEN": api_token}
    request = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode('utf8'))

        repos = []
        for repo in data:
            repos.append(repo["http_url_to_repo"])
        return repos

# --- Main prog
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 gitlab-forks.py <gitlab_instance> <repo_id> <token>")
        print()
        print(" <gitlab_instance>: GitLab instance, for example 'https://gitlab.etsit.urjc.es'")
        print(" <repo_id>: Repository ID, for example '2799'")
        print(" <token>: GitLab API token")
        sys.exit(1)

    forks = get_forks(gitlab_instance=sys.argv[1],
                      repo_id=sys.argv[2], api_token=sys.argv[3])
    print(json.dumps(forks, indent=2))
