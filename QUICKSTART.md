# 🚀 Quick Start - Get Running in 5 Minutes

## Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed
- Git installed
- GitHub account (or GitLab/Jenkins)
- OpenAI API key

## Step 1: Clone & Setup (2 minutes)

```bash
# Run the setup script
./setup.sh  # Linux/Mac
# OR
.\setup.ps1  # Windows PowerShell
```

## Step 2: Configure (2 minutes)

1. **Get your tokens**:
   - GitHub: https://github.com/settings/tokens (need `repo` + `workflow` scopes)
   - OpenAI: https://platform.openai.com/api-keys

2. **Edit `.env`**:
   ```bash
   # Minimum required configuration
   GITHUB_TOKEN=ghp_your_github_token_here
   OPENAI_API_KEY=sk-your_openai_key_here
   AUTO_FIX_ENABLED=true
   AUTO_COMMIT_ENABLED=true
   ```

## Step 3: Run (1 minute)

### Option A: Docker (Easiest)
```bash
docker-compose up
```

### Option B: Manual
```bash
# Terminal 1 - Backend
cd agent-core
python main.py

# Terminal 2 - Dashboard
cd dashboard
npm run dev
```

## Step 4: Test It!

1. **Open Dashboard**: http://localhost:3000

2. **Trigger a test failure**:
   - Push a commit with a failing test to any repo
   - Or create a syntax error in a CI workflow

3. **Watch the magic**:
   - Agent detects failure (within 30 seconds)
   - Analyzes the error
   - Generates a fix
   - Commits and re-runs pipeline
   - Check dashboard for results!

## Verify It's Working

Check the logs:
```bash
tail -f agent-core/agent.log
```

You should see:
```
✓ GitHub monitor initialized
✓ Starting pipeline monitoring...
✓ Running monitoring cycle...
```

## Common Issues

**"No monitors configured"**
- Add your GITHUB_TOKEN to .env

**"OpenAI API error"**
- Verify your OPENAI_API_KEY is correct
- Check you have API credits

**Dashboard shows no data**
- Wait 30 seconds for first polling cycle
- Trigger a pipeline failure to see activity

## What's Next?

- Read [Getting Started Guide](docs/getting-started.md) for details
- Customize `config/agent-config.yaml`
- Add more CI/CD platforms
- Check the dashboard for analytics

## Need Help?

- Check `docs/` folder for detailed guides
- Review `PROJECT_SUMMARY.md` for architecture
- See example workflow in `.github/workflows/`

---

**That's it! You now have an AI agent automatically fixing your CI/CD failures! 🎉**
