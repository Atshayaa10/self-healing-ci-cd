# 🤖 AI-Powered Self-Healing CI/CD Agent

> Automatically detect, analyze, and fix CI/CD pipeline failures using AI - no human intervention required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

## 🎯 Problem

CI/CD pipelines fail frequently due to:
- Dependency conflicts
- Broken tests
- Configuration errors
- Environment issues
- Syntax errors

Developers waste hours manually debugging, fixing, and re-running pipelines.

## 💡 Solution

An intelligent agent that:
1. **Monitors** your CI/CD pipelines in real-time
2. **Analyzes** failures using AI to determine root cause
3. **Generates** appropriate fixes automatically
4. **Applies** fixes and re-triggers pipelines
5. **Learns** from successful fixes to improve over time

## ✨ Features

- 🔍 **Real-time Monitoring** - Continuous pipeline surveillance
- 🧠 **AI-Powered Analysis** - GPT-4 powered root cause detection
- 🔧 **Automated Fixes** - Smart repair generation and application
- 🔄 **Auto-Commit & Re-run** - Seamless fix deployment
- 📊 **Analytics Dashboard** - Track success rates and trends
- 🔌 **Multi-Platform** - GitHub Actions, GitLab CI, Jenkins
- 📈 **Success Tracking** - Monitor fix effectiveness

## 🚀 Quick Start

**Get running in 5 minutes!** See [QUICKSTART.md](QUICKSTART.md)

```bash
# 1. Setup
./setup.sh  # or setup.ps1 on Windows

# 2. Configure
cp .env.example .env
# Add your GITHUB_TOKEN and OPENAI_API_KEY

# 3. Run
docker-compose up
# OR manually: python agent-core/main.py

# 4. Open dashboard
# http://localhost:3000
```

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (optional but recommended)
- CI/CD platform account (GitHub/GitLab/Jenkins)
- OpenAI API key

## 🏗️ Architecture

```
┌─────────────────┐
│  CI/CD Platform │ (GitHub/GitLab/Jenkins)
└────────┬────────┘
         │ Monitors
         ▼
┌─────────────────┐
│  Agent Core     │
│  - Orchestrator │
│  - Monitors     │
│  - Analyzer     │──► OpenAI GPT-4
│  - Fix Engine   │
│  - Git Manager  │
└────────┬────────┘
         │ Stores
         ▼
┌─────────────────┐
│    Database     │ (SQLite/PostgreSQL)
└─────────────────┘
         │ Serves
         ▼
┌─────────────────┐
│    Dashboard    │ (React)
└─────────────────┘
```

## 📚 Documentation

- 📖 [Getting Started Guide](docs/getting-started.md)
- 🏛️ [Architecture Overview](docs/architecture.md)
- 🔌 [Integration Guide](docs/integrations.md)
- 🔧 [API Reference](docs/api.md)
- 🤝 [Contributing](CONTRIBUTING.md)

## 🎨 Dashboard Preview

The dashboard provides:
- Real-time pipeline monitoring
- Failure analysis details
- Fix history and success rates
- System statistics and trends

## 🔧 Configuration

Customize behavior in `config/agent-config.yaml`:

```yaml
agent:
  polling_interval: 30  # seconds
  max_concurrent_fixes: 5

auto_fix:
  enabled: true
  strategies:
    dependency_conflict: [update_version, pin_version]
    test_failure: [fix_assertion, update_mock]
    syntax_error: [auto_format, fix_import]
```

## 🧪 Supported Error Types

| Category | Detection | Auto-Fix |
|----------|-----------|----------|
| Dependency Conflicts | ✅ | ✅ |
| Test Failures | ✅ | ⚠️ Manual Review |
| Syntax Errors | ✅ | ✅ |
| Configuration Errors | ✅ | ✅ |
| Environment Issues | ✅ | ✅ |
| Timeouts | ✅ | ⚠️ Partial |
| Resource Limits | ✅ | ⚠️ Partial |

## 🔐 Security

- Credentials stored securely in environment variables
- Repository access limited to necessary permissions
- All fixes logged for audit trail
- Optional manual approval for critical changes

## 📊 Success Metrics

Track your agent's performance:
- Total pipelines monitored
- Failures detected and analyzed
- Fixes applied successfully
- Overall success rate
- Time saved vs manual debugging

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, OpenAI API, GitPython  
**Frontend:** React, TypeScript, Vite, TanStack Query  
**Infrastructure:** Docker, Nginx, PostgreSQL/SQLite

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built to solve real developer pain points in CI/CD workflows.

---

**Ready to stop manually fixing CI/CD failures?** [Get Started Now →](QUICKSTART.md)
