import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-core'))

from app.core.config import settings
import requests

# Test GitHub token permissions
token = settings.GITHUB_TOKEN
if not token:
    print("ERROR: No GitHub token found in .env")
    sys.exit(1)

print(f"Testing token: {token[:20]}...")

# Test 1: Check token validity
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get('https://api.github.com/user', headers=headers)
print(f"\n1. Token validity: {response.status_code}")
if response.status_code == 200:
    user_data = response.json()
    print(f"   Authenticated as: {user_data.get('login')}")
else:
    print(f"   Error: {response.text}")
    sys.exit(1)

# Test 2: Check token scopes
scopes = response.headers.get('X-OAuth-Scopes', '')
print(f"\n2. Token scopes: {scopes}")

# Test 3: Check repository access
repo = 'Atshayaa10/sample_file_ci_cd'
response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
print(f"\n3. Repository access: {response.status_code}")
if response.status_code == 200:
    repo_data = response.json()
    print(f"   Repository: {repo_data.get('full_name')}")
    print(f"   Permissions:")
    perms = repo_data.get('permissions', {})
    print(f"     - admin: {perms.get('admin', False)}")
    print(f"     - push: {perms.get('push', False)}")
    print(f"     - pull: {perms.get('pull', False)}")
    
    if not perms.get('push', False):
        print("\n   ⚠️  WARNING: Token does NOT have push permission!")
        print("   You need to regenerate the token with 'Contents' write permission")
else:
    print(f"   Error: {response.text}")

# Test 4: Try to get a file from the repo
response = requests.get(f'https://api.github.com/repos/{repo}/contents/app.py', headers=headers)
print(f"\n4. File access (app.py): {response.status_code}")
if response.status_code == 200:
    print("   ✓ Can read files")
else:
    print(f"   Error: {response.text}")

print("\n" + "="*60)
print("SUMMARY:")
print("="*60)
if scopes and 'repo' in scopes:
    print("✓ Token has 'repo' scope")
elif scopes and 'public_repo' in scopes:
    print("✓ Token has 'public_repo' scope")
else:
    print("✗ Token missing required scopes")
    print("  Required: 'repo' or 'public_repo' + 'workflow'")
