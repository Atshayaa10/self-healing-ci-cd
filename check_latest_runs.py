import os
from github import Github
from dotenv import load_dotenv

# Load environment
load_dotenv('agent-core/.env')

token = os.getenv('GITHUB_TOKEN')
g = Github(token)

# Get sample_file_ci_cd repo
repos = list(g.get_user().get_repos())
target_repo = None

for repo in repos:
    if 'sample_file_ci_cd' in repo.name:
        target_repo = repo
        break

if not target_repo:
    print("sample_file_ci_cd repo not found!")
    exit(1)

print(f"Repository: {target_repo.full_name}")
print(f"\nLast 10 workflow runs:")
print("-" * 80)

workflows = target_repo.get_workflow_runs()
for i, run in enumerate(list(workflows)[:10]):
    print(f"{i+1}. Run ID: {run.id}")
    print(f"   Status: {run.status} | Conclusion: {run.conclusion}")
    print(f"   Branch: {run.head_branch}")
    print(f"   Created: {run.created_at}")
    print(f"   Updated: {run.updated_at}")
    print()
