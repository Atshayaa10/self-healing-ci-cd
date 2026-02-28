#!/usr/bin/env python3
"""Test GitHub connection and list workflows"""

from github import Github
import os

# Read .env file manually
env_path = 'agent-core/.env' if os.path.exists('agent-core/.env') else '.env'

token = None
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('GITHUB_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break

if not token:
    print("❌ GITHUB_TOKEN not found in .env file")
    exit(1)

print(f"✅ Token found: {token[:20]}...")

try:
    # Create GitHub client
    g = Github(token)
    
    # Get user info
    user = g.get_user()
    print(f"\n✅ Connected as: {user.login}")
    print(f"✅ Name: {user.name}")
    
    # List repositories
    print(f"\n📦 Your repositories:")
    repos = list(user.get_repos())
    
    if not repos:
        print("❌ No repositories found!")
        print("Make sure your token has 'repo' scope")
        exit(1)
    
    for i, repo in enumerate(repos[:10], 1):
        print(f"  {i}. {repo.full_name}")
        
        # Check for workflows
        try:
            workflows = list(repo.get_workflow_runs())
            if workflows:
                print(f"     └─ {len(workflows)} workflow runs found")
                
                # Check for failures
                failed = [w for w in workflows[:10] if w.status == "completed" and w.conclusion == "failure"]
                if failed:
                    print(f"     └─ ⚠️  {len(failed)} FAILED workflows!")
                    for fw in failed[:3]:
                        print(f"        - Run #{fw.id}: {fw.name} (Branch: {fw.head_branch})")
                else:
                    print(f"     └─ ✅ No failed workflows in last 10 runs")
            else:
                print(f"     └─ No workflows found")
        except Exception as e:
            print(f"     └─ Error checking workflows: {e}")
    
    print("\n" + "="*50)
    print("✅ GitHub connection test complete!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid token")
    print("2. Token doesn't have 'repo' and 'workflow' scopes")
    print("3. Network connectivity issue")
