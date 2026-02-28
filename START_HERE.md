# 🚀 START HERE - Quick Setup for Windows

## You're Almost Ready!

Since Docker isn't installed, let's use the manual setup. It's easy!

## Step 1: Configure Your Credentials (2 minutes)

1. Open the `.env` file that was just created:
   ```powershell
   notepad .env
   ```

2. Add your credentials:
   ```env
   # Required: Get from https://github.com/settings/tokens
   GITHUB_TOKEN=ghp_your_token_here
   
   # Required: Get from https://platform.openai.com/api-keys
   OPENAI_API_KEY=sk-your_key_here
   
   # Optional: Enable auto-fixing
   AUTO_FIX_ENABLED=true
   AUTO_COMMIT_ENABLED=true
   ```

3. Save and close

### How to Get Tokens:

**GitHub Token:**
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scopes: `repo` and `workflow`
- Copy the token

**OpenAI API Key:**
- Go to: https://platform.openai.com/api-keys
- Sign up or log in
- Click "Create new secret key"
- Copy the key

## Step 2: Start the Backend (1 minute)

Open PowerShell in this folder and run:

```powershell
.\start-backend.ps1
```

If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see:
```
✅ Starting agent on http://localhost:8000
INFO: Starting AI-Powered Self-Healing CI/CD Agent
```

**Keep this terminal open!**

## Step 3: Start the Dashboard (1 minute)

Open a NEW PowerShell window in this folder and run:

```powershell
.\start-dashboard.ps1
```

You should see:
```
✅ Starting dashboard on http://localhost:3000
VITE ready in XXX ms
```

**Keep this terminal open too!**

## Step 4: Open the Dashboard

Open your browser and go to:
```
http://localhost:3000
```

You should see the dashboard! 🎉

## Step 5: Test It!

1. The agent is now monitoring your GitHub repositories
2. Trigger a test failure in any repo (or wait for a real failure)
3. Watch the dashboard update with:
   - Detected failure
   - AI analysis
   - Generated fix
   - Success metrics

## Troubleshooting

### Backend won't start?

Check:
- Is Python installed? `python --version`
- Is .env configured with valid tokens?
- Is port 8000 available?

### Dashboard won't start?

Check:
- Is Node.js installed? `node --version`
- Did npm install complete successfully?
- Is port 3000 available?

### Need more help?

- See **WINDOWS_SETUP_GUIDE.md** for detailed instructions
- Check **FAQ.md** for common questions
- Review **docs/getting-started.md** for full documentation

## Quick Commands

### Check if backend is running:
```powershell
curl http://localhost:8000/health
```

### View backend logs:
```powershell
Get-Content agent-core\agent.log -Tail 20
```

### Stop everything:
Press `Ctrl+C` in both terminal windows

## What's Next?

Once everything is running:

1. ✅ Backend: http://localhost:8000
2. ✅ Dashboard: http://localhost:3000
3. 📊 View statistics and metrics
4. 🔍 Monitor pipeline failures
5. 🤖 Watch automatic fixes being applied

---

**You're all set! The agent is now protecting your CI/CD pipelines! 🚀**
