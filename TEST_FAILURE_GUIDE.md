# 🧪 Testing Your Self-Healing Agent

## Quick Test: Create a Failing Pipeline

### Method 1: Create a Test Repository (Easiest)

1. **Go to GitHub and create a new repository:**
   - Name: `ci-healer-test`
   - Make it public or private
   - Initialize with README

2. **Add a GitHub Actions workflow:**
   
   Create file: `.github/workflows/test.yml`
   
   ```yaml
   name: Test CI
   
   on: [push]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Failing test
           run: |
             echo "This will fail"
             exit 1
   ```

3. **Commit and push:**
   - The workflow will run and fail
   - Within 30 seconds, your agent will detect it!

4. **Check your dashboard:**
   - Refresh http://localhost:3000
   - You should see the failure appear
   - Check the "Failures" tab for analysis
   - Check the "Fixes" tab for the generated fix

---

### Method 2: Break an Existing Repository (Temporary)

If you have an existing repo with CI/CD:

1. **Create a syntax error in a test file:**
   ```python
   # In any Python test file
   def test_something()  # Missing colon
       assert True
   ```

2. **Or create a dependency conflict:**
   ```txt
   # In requirements.txt
   requests==2.28.0
   urllib3==2.0.0  # Conflicts with requests
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Test CI healing"
   git push
   ```

4. **Watch the agent work:**
   - Pipeline fails
   - Agent detects it (within 30 seconds)
   - Analyzes the error
   - Generates a fix
   - Commits the fix (if AUTO_COMMIT_ENABLED=true)
   - Re-runs the pipeline

---

### Method 3: Use the Example Workflow

1. **In your test repository, add this workflow:**

   `.github/workflows/dependency-test.yml`
   
   ```yaml
   name: Dependency Test
   
   on: [push]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         
         - name: Create requirements with conflict
           run: |
             echo "requests==2.28.0" > requirements.txt
             echo "urllib3==2.0.0" >> requirements.txt
         
         - name: Install dependencies (will fail)
           run: pip install -r requirements.txt
   ```

2. **Commit and push**

3. **Watch the magic happen!**

---

## 📊 What You'll See

### In the Dashboard:

1. **Dashboard Tab:**
   - Total Pipelines: 1
   - Total Failures: 1
   - Successful Fixes: 0 (or 1 after fix)
   - Success Rate: Updates in real-time

2. **Pipelines Tab:**
   - Your repository name
   - Branch name
   - Commit SHA
   - Status: "failure"

3. **Failures Tab:**
   - Error category (e.g., "dependency_conflict")
   - Error message
   - Root cause analysis from AI
   - Confidence score

4. **Fixes Tab:**
   - Fix type
   - Description
   - Status (pending/applied/verified)
   - Commit SHA (if applied)

### In the Backend Terminal:

```
INFO: Handling failure: 12345
INFO: Analyzing error...
INFO: Error category: dependency_conflict
INFO: Generating fix...
INFO: Fix generated: dependency_conflict_resolution
INFO: Applying fix...
INFO: Committed fix: abc123
INFO: Re-triggered pipeline
```

---

## 🎮 Interactive Testing

### Test Different Error Types:

1. **Syntax Error:**
   ```python
   # test.py
   def hello()  # Missing colon
       print("Hello")
   ```

2. **Test Failure:**
   ```python
   # test_example.py
   def test_math():
       assert 1 + 1 == 3  # Wrong assertion
   ```

3. **Configuration Error:**
   ```yaml
   # .github/workflows/broken.yml
   name: Broken
   on: push
   jobs:
     test:
       runs-on: ubuntu-latest
       # Missing steps
   ```

4. **Environment Issue:**
   ```yaml
   steps:
     - name: Use undefined variable
       run: echo $UNDEFINED_VAR
   ```

---

## 🔍 Monitoring the Agent

### Check Agent Logs:

```powershell
# In a new terminal
Get-Content C:\Users\atsha\self-healing-cicd\agent-core\agent.log -Tail 50 -Wait
```

### Check API Directly:

```powershell
# Get statistics
curl http://localhost:8000/api/v1/stats

# Get pipelines
curl http://localhost:8000/api/v1/pipelines

# Get failures
curl http://localhost:8000/api/v1/failures

# Get fixes
curl http://localhost:8000/api/v1/fixes
```

---

## ⚙️ Configuration Options

### Adjust Monitoring Speed:

Edit `config/agent-config.yaml`:

```yaml
agent:
  polling_interval: 10  # Check every 10 seconds instead of 30
```

### Enable/Disable Auto-Fix:

Edit `.env`:

```env
# Generate fixes but don't apply them
AUTO_FIX_ENABLED=true
AUTO_COMMIT_ENABLED=false

# Or disable everything
AUTO_FIX_ENABLED=false
```

### Change AI Model:

Edit `.env`:

```env
# Use cheaper model
AI_MODEL=gpt-3.5-turbo

# Or use GPT-4
AI_MODEL=gpt-4
```

---

## 🎯 Success Criteria

Your agent is working correctly if:

✅ Dashboard loads and shows statistics
✅ Backend logs show "Running monitoring cycle"
✅ When you create a failure, it appears in dashboard within 30 seconds
✅ Failure analysis shows error category and root cause
✅ Fix is generated and shown in Fixes tab
✅ If auto-commit enabled, fix is committed to repo

---

## 🐛 Troubleshooting

### "No data available" persists:

1. **Check if agent is monitoring:**
   - Look at backend terminal logs
   - Should see "Running monitoring cycle" every 30 seconds

2. **Verify GitHub token:**
   - Check `.env` has valid GITHUB_TOKEN
   - Token should start with `ghp_`
   - Token needs `repo` and `workflow` scopes

3. **Check if you have repositories:**
   - Agent only monitors repos you have access to
   - Create a test repo if needed

4. **Trigger a test failure:**
   - Create a simple failing workflow
   - Wait 30 seconds
   - Check dashboard

### Agent not detecting failures:

1. **Check polling interval:**
   - Default is 30 seconds
   - Wait at least 30 seconds after failure

2. **Check repository access:**
   - Token must have access to the repo
   - Repo must have GitHub Actions enabled

3. **Check logs:**
   - Look for errors in backend terminal
   - Check `agent.log` file

---

## 📈 Next Steps After Testing

Once you see it working:

1. **Monitor your real repositories**
2. **Adjust configuration** based on your needs
3. **Review fix success rate** in dashboard
4. **Fine-tune auto-commit settings**
5. **Add more repositories** to monitor
6. **Set up notifications** (future feature)

---

## 🎉 You're Done!

Your AI-Powered Self-Healing CI/CD Agent is now:
- ✅ Running and monitoring
- ✅ Ready to detect failures
- ✅ Ready to analyze errors with AI
- ✅ Ready to generate and apply fixes
- ✅ Tracking everything in the dashboard

**The system is complete and fully functional!**
