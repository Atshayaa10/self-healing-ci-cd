# Frequently Asked Questions (FAQ)

## General Questions

### What is the Self-Healing CI/CD Agent?

An AI-powered system that automatically detects, analyzes, and fixes CI/CD pipeline failures without human intervention. It monitors your pipelines, uses AI to understand what went wrong, generates appropriate fixes, and applies them automatically.

### How does it work?

1. Monitors your CI/CD pipelines continuously
2. Detects when a pipeline fails
3. Fetches and analyzes error logs using AI
4. Classifies the error type
5. Generates an appropriate fix
6. Commits the fix to your repository
7. Re-triggers the pipeline
8. Tracks success/failure

### What CI/CD platforms are supported?

Currently supported:
- GitHub Actions
- GitLab CI
- Jenkins

Planned for future releases:
- CircleCI
- Travis CI
- Azure DevOps
- Bitbucket Pipelines

### What types of errors can it fix?

- Dependency conflicts (version mismatches)
- Syntax errors (missing semicolons, brackets, etc.)
- Configuration errors (invalid YAML, missing keys)
- Environment issues (missing variables)
- Import/module errors
- Some test failures (with caution)

### Is it safe to use in production?

The agent is functional but consider:
- Start with non-critical repositories
- Review fixes before enabling auto-commit
- Use manual approval for critical changes
- Monitor the agent's success rate
- Keep backups of your repositories

---

## Setup & Configuration

### What do I need to get started?

**Required:**
- Python 3.9+
- Node.js 18+
- CI/CD platform account (GitHub/GitLab/Jenkins)
- OpenAI API key

**Optional:**
- Docker (recommended)
- Domain name (for production)
- SSL certificate (for HTTPS)

### How do I get a GitHub token?

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo` and `workflow`
4. Copy the token and add to `.env` as `GITHUB_TOKEN`

### How do I get an OpenAI API key?

1. Go to https://platform.openai.com/api-keys
2. Create an account or sign in
3. Click "Create new secret key"
4. Copy the key and add to `.env` as `OPENAI_API_KEY`
5. Ensure you have API credits

### Can I use a different AI provider?

Yes! The system supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)

Set `ANTHROPIC_API_KEY` in `.env` to use Claude instead.

### How much does it cost to run?

**Infrastructure:**
- Self-hosted: Free (your server costs)
- Docker: Free
- Cloud hosting: Varies by provider

**AI API Costs:**
- OpenAI GPT-4: ~$0.03 per 1K tokens
- OpenAI GPT-3.5: ~$0.002 per 1K tokens
- Typical analysis: 500-1000 tokens
- Estimated: $1-5 per 100 failures analyzed

### Can I run it without Docker?

Yes! Follow the manual installation:
```bash
cd agent-core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Usage Questions

### How often does it check for failures?

Default: Every 30 seconds

Customize in `config/agent-config.yaml`:
```yaml
agent:
  polling_interval: 30  # seconds
```

### Will it fix every failure automatically?

No. Behavior depends on configuration:
- `AUTO_FIX_ENABLED`: Generate fixes
- `AUTO_COMMIT_ENABLED`: Apply fixes automatically

Some error types (like test failures) may require manual review.

### How do I disable auto-commit?

In `.env`:
```env
AUTO_COMMIT_ENABLED=false
```

The agent will still analyze and generate fixes, but won't commit them automatically.

### Can I review fixes before they're applied?

Yes! Set `AUTO_COMMIT_ENABLED=false` and review fixes in the dashboard before manually applying them.

### What if the agent makes a mistake?

- All fixes are logged in the database
- Commit messages are tagged with "🤖 Auto-fix"
- You can revert commits using git
- Review the dashboard for fix history
- Adjust configuration to prevent similar issues

### How do I monitor the agent's activity?

1. **Dashboard**: http://localhost:3000
2. **Logs**: `tail -f agent-core/agent.log`
3. **API**: `curl http://localhost:8000/api/v1/stats`

---

## Troubleshooting

### Agent not detecting failures

**Check:**
- Is your CI/CD token valid?
- Does the token have correct permissions?
- Are you monitoring the right repositories?
- Check logs: `tail -f agent-core/agent.log`

**Solution:**
```bash
# Verify token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Check agent logs
docker-compose logs agent
```

### Dashboard shows no data

**Check:**
- Is the backend running? `curl http://localhost:8000/health`
- Wait 30 seconds for first polling cycle
- Trigger a test failure to generate data
- Check browser console for errors

### Fixes not being applied

**Check:**
- `AUTO_FIX_ENABLED=true` in `.env`
- `AUTO_COMMIT_ENABLED=true` in `.env`
- Agent has write access to repository
- Check logs for git errors

### OpenAI API errors

**Common issues:**
- Invalid API key
- Insufficient credits
- Rate limit exceeded
- Network connectivity

**Solution:**
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

### High memory usage

**Solutions:**
- Reduce polling frequency
- Limit concurrent fixes in config
- Use PostgreSQL instead of SQLite
- Restart the agent periodically

### Database errors

**SQLite locked:**
- Switch to PostgreSQL for production
- Reduce concurrent operations

**Migration issues:**
- Delete `agent.db` and restart (loses data)
- Or backup and restore

---

## Advanced Questions

### Can I customize fix strategies?

Yes! Edit `agent-core/app/services/fix_engine.py`:

```python
async def _fix_dependency_conflict(self, analysis, context):
    # Add your custom logic here
    pass
```

### Can I add support for other CI/CD platforms?

Yes! Create a new monitor:

1. Create `agent-core/app/services/monitors/your_platform_monitor.py`
2. Inherit from `BaseMonitor`
3. Implement required methods
4. Register in `AgentOrchestrator`

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### How do I scale for multiple teams?

**Current (v1.0):**
- Single instance per team
- Separate configurations
- Isolated databases

**Future (v2.0+):**
- Multi-tenant support
- Organization management
- Resource quotas

### Can I use it with private repositories?

Yes! The agent works with private repositories as long as your access token has the necessary permissions.

### How do I backup the data?

**SQLite:**
```bash
cp agent-core/agent.db backup.db
```

**PostgreSQL:**
```bash
pg_dump -U user ci_healer > backup.sql
```

### Can I run multiple agents?

Yes, but:
- Use different databases
- Avoid monitoring same repositories
- Or implement distributed locking (future feature)

### How do I update to a new version?

```bash
git pull origin main
docker-compose build
docker-compose up -d
```

### Can I contribute to the project?

Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Security Questions

### Is my code safe?

- Agent only reads logs and writes fixes
- All operations are logged
- You control what gets auto-committed
- Review fixes before enabling auto-commit
- Use separate tokens with limited permissions

### Where are credentials stored?

- In `.env` file (not committed to git)
- Use environment variables
- For production, use secrets management (AWS Secrets Manager, etc.)

### Can others see my pipeline data?

No. The agent runs on your infrastructure and data stays with you. Nothing is sent to external services except:
- OpenAI API (for error analysis only)
- Your CI/CD platform APIs

### What data is sent to OpenAI?

Only:
- Error logs (truncated to 2000 characters)
- Error category
- Basic context

Not sent:
- Full source code
- Credentials
- Sensitive data

### How do I secure the dashboard?

Currently no built-in authentication. For production:
- Use reverse proxy with authentication
- Restrict network access
- Use VPN
- Or wait for v2.0 with built-in auth

---

## Performance Questions

### How many repositories can it monitor?

Depends on:
- Polling interval
- Server resources
- API rate limits

Tested with:
- 50+ repositories
- 30-second polling
- 2GB RAM, 2 CPU cores

### What are the resource requirements?

**Minimum:**
- 1GB RAM
- 1 CPU core
- 10GB disk

**Recommended:**
- 2GB RAM
- 2 CPU cores
- 50GB disk

### How fast does it fix issues?

Typical timeline:
- Detection: 0-30 seconds (polling interval)
- Analysis: 5-10 seconds
- Fix generation: 5-15 seconds
- Application: 5-10 seconds
- Total: 15-65 seconds

### Can I make it faster?

Yes:
- Reduce polling interval (increases API calls)
- Use GPT-3.5 instead of GPT-4 (faster, cheaper)
- Optimize database queries
- Use caching

---

## Comparison Questions

### How is this different from Dependabot?

**Dependabot:**
- Only handles dependency updates
- Creates PRs for review
- Scheduled updates

**Self-Healing Agent:**
- Handles all error types
- Fixes failures automatically
- Real-time monitoring
- AI-powered analysis

### How is this different from GitHub Copilot?

**Copilot:**
- Code completion tool
- Helps write code
- IDE integration

**Self-Healing Agent:**
- Fixes CI/CD failures
- Automated operation
- No IDE needed
- Monitors pipelines

### Should I use this instead of manual debugging?

Use both:
- Agent handles common, repetitive issues
- You focus on complex problems
- Agent learns from your fixes
- Saves time on routine failures

---

## Future Features

### What's coming next?

See [ROADMAP.md](ROADMAP.md) for detailed plans:
- Learning from historical fixes
- More CI/CD platforms
- Team collaboration features
- Advanced analytics
- Authentication system

### Can I request a feature?

Yes! Open an issue on GitHub with:
- Feature description
- Use case
- Expected behavior
- Examples

### When will [feature] be available?

Check [ROADMAP.md](ROADMAP.md) for timeline. Dates are approximate and subject to change.

---

## Getting Help

### Where can I get support?

1. Check this FAQ
2. Read the [documentation](docs/)
3. Review [examples](examples/)
4. Open a GitHub issue
5. Check existing issues

### How do I report a bug?

Open a GitHub issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Logs and error messages
- Environment details

### How do I suggest improvements?

Open a GitHub issue with the `enhancement` label and describe your suggestion.

---

**Still have questions?** Open an issue on GitHub!
