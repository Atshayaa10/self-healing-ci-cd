import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-core'))

from app.core.config import settings
import requests

token = settings.GITHUB_TOKEN
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Get workflow runs for sample_file_ci_cd
repo = 'Atshayaa10/sample_file_ci_cd'
url = f'https://api.github.com/repos/{repo}/actions/runs'
params = {
    'status': 'failure',
    'per_page': 10
}

print(f"Checking failed workflows for {repo}...")
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    runs = data.get('workflow_runs', [])
    print(f"\nFound {len(runs)} failed workflow runs:")
    for run in runs:
        print(f"  - ID: {run['id']}")
        print(f"    Name: {run['name']}")
        print(f"    Status: {run['status']} / {run['conclusion']}")
        print(f"    Created: {run['created_at']}")
        print()
else:
    print(f"Error: {response.status_code}")
    print(response.text)
