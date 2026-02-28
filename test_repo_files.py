import sys
sys.path.insert(0, 'agent-core')
from app.services.git_manager import GitManager
import tempfile
import os

gm = GitManager()
repo_path = gm.clone_repository('https://github.com/Atshayaa10/sample_file_ci_cd.git', tempfile.mkdtemp())

print('Files in repo:')
for root, dirs, files in os.walk(repo_path):
    # Skip .git directory
    if '.git' in root:
        continue
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), repo_path)
        print(f"  {rel_path}")

print(f"\nRepo path: {repo_path}")
