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
print(f"\nLast 5 commits on main branch:")
print("-" * 80)

commits = target_repo.get_commits(sha='main')
for i, commit in enumerate(list(commits)[:5]):
    print(f"{i+1}. SHA: {commit.sha[:8]}")
    print(f"   Message: {commit.commit.message.split(chr(10))[0]}")
    print(f"   Author: {commit.commit.author.name}")
    print(f"   Date: {commit.commit.author.date}")
    print()
