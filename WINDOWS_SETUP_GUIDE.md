# Windows Setup Guide

## Option 1: Install Docker Desktop (Recommended)

### Step 1: Install Docker Desktop

1. Download Docker Desktop for Windows:
   https://www.docker.com/products/docker-desktop/

2. Run the installer and follow the prompts

3. Restart your computer if prompted

4. Open Docker Desktop and wait for it to start

5. Verify installation:
   ```powershell
   docker --version
   docker compose version
   ```

### Step 2: Run the Project

```powershell
# Configure environment
cp .env.example .env
# Edit .env with your tokens

# Start with Docker
docker compose up
```

---

## Option 2: Manual Setup (No Docker Required)

### Prerequisites

1. **Install Python 3.9+**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Install Node.js 18+**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **Install Git**
   - Download from: https://git-scm.com/download/win
   - Verify: `git --version`

### Step-by-Step Setup

#### 1. Configure Environment

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env file with your credentials
notepad .env
```

Add your tokens:
```env
GITHUB_TOKEN=ghp_your_github_token_here
OPENAI_API_KEY=sk-your_openai_key_here
AUTO_FIX_ENABLED=true
AUTO_COMMIT_ENABLED=true
```

#### 2. Setup Backend

```powershell
# Navigate to backend
cd agent-core

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Start the backend (keep this terminal open)
python main.py
```

You should see:
```
INFO: Starting AI-Powered Self-Healing CI/CD Agent
INFO: Agent started on port 8000
```

#### 3. Setup Dashboard (New Terminal)

Open a NEW PowerShell terminal:

```powershell
# Navigate to dashboard
cd dashboard

# Install dependencies
npm install

# Start the dashboard (keep this terminal open)
npm run dev
```

You should see:
```
VITE ready in XXX ms
Local: http://localhost:3000
```

#### 4. Access the Dashboard

Open your browser and go to:
```
http://localhost:3000
```

### Troubleshooting

#### Python not found
```powershell
# Check if Python is installed
python --version

# If not found, download from python.org
# Make sure to check "Add Python to PATH" during installation
```

#### Cannot activate virtual environment
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1
```

#### Port already in use
```powershell
# Backend (port 8000)
netstat -ano | findstr :8000
# Kill the process using the PID shown

# Dashboard (port 3000)
netstat -ano | findstr :3000
# Kill the process using the PID shown
```

#### Module not found errors
```powershell
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt
```

### Stopping the Application

To stop the application:

1. In the backend terminal: Press `Ctrl+C`
2. In the dashboard terminal: Press `Ctrl+C`

### Restarting the Application

```powershell
# Terminal 1 - Backend
cd agent-core
.\venv\Scripts\Activate.ps1
python main.py

# Terminal 2 - Dashboard
cd dashboard
npm run dev
```

---

## Quick Reference

### Backend Commands
```powershell
cd agent-core
.\venv\Scripts\Activate.ps1
python main.py
```

### Dashboard Commands
```powershell
cd dashboard
npm run dev
```

### Check if Running
```powershell
# Backend health check
curl http://localhost:8000/health

# Or in browser
http://localhost:8000/health
```

### View Logs
```powershell
# Backend logs
Get-Content agent-core\agent.log -Tail 50 -Wait
```

---

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Dashboard running on http://localhost:3000
3. 🎯 Trigger a test pipeline failure
4. 👀 Watch the agent detect and fix it
5. 📊 Check the dashboard for results

---

## Getting Tokens

### GitHub Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` and `workflow`
4. Copy token and add to `.env`

### OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy key and add to `.env`
4. Ensure you have API credits

---

## Common Issues

### "Python is not recognized"
- Reinstall Python and check "Add to PATH"
- Or add Python to PATH manually

### "npm is not recognized"
- Reinstall Node.js
- Restart PowerShell after installation

### "Cannot load module" error
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Backend won't start
- Check if port 8000 is available
- Verify .env file exists and has correct values
- Check agent.log for errors

### Dashboard won't start
- Check if port 3000 is available
- Delete node_modules and run `npm install` again
- Check for npm errors

---

## Need Help?

- Check FAQ.md for common questions
- Review docs/getting-started.md for detailed info
- Check examples/test-scenarios.md for testing
