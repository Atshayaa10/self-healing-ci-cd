# Fix GitHub Token Permissions

Your token has 403 "Permission denied" errors when pushing. This means the fine-grained token needs specific permissions.

## Steps to Fix:

### 1. Go to GitHub Token Settings
Visit: https://github.com/settings/tokens?type=beta

### 2. Find Your Current Token
Look for the token starting with `github_pat_11BQJTWII...`

### 3. Click "Regenerate token" or Create New Token

### 4. Set These Permissions:

**Repository access:**
- Select: "Only select repositories"
- Choose: `Atshayaa10/sample_file_ci_cd` (and any other repos you want to fix)

**Repository permissions:**
- ✅ **Contents**: Read and write (CRITICAL - this allows pushing code)
- ✅ **Workflows**: Read and write (allows modifying workflow files)
- ✅ **Metadata**: Read-only (automatically selected)
- ✅ **Actions**: Read and write (optional, for triggering workflows)

### 5. Generate Token

Click "Generate token" and copy the new token.

### 6. Update Your .env File

Replace the token in `agent-core/.env`:

```
GITHUB_TOKEN=your_new_token_here
```

### 7. Restart the Backend

```powershell
# In agent-core directory
python main.py
```

## Why This is Needed:

Fine-grained tokens are more secure but require explicit permissions. The key permission is:
- **Contents: Read and write** - This allows the agent to push commits to your repository

Without this permission, you'll get "403 Permission denied" errors even though the token can read the repository.

## Verify Token Permissions:

After updating, run:
```powershell
cd agent-core
.\venv\Scripts\Activate.ps1
python ..\test_token_permissions.py
```

You should see:
- ✓ Token has push permission: True
- ✓ Can read files
