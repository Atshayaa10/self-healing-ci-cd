# PR Feature - Quick Start Guide

## ✅ Status: FULLY IMPLEMENTED & CONNECTED

The risk-based PR creation feature is now complete and integrated into the system.

## 🎯 Quick Test (5 Minutes)

### 1. Create Test File
In your `sample_file_ci_cd` repo, create `test_pr.py`:
```python
def hello()  # Missing colon - LOW RISK
    print("Hello")

hello()
```

### 2. Create Workflow
Create `.github/workflows/test_pr.yml`:
```yaml
name: Test PR Feature
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python test_pr.py
```

### 3. Push & Watch
```bash
git add .
git commit -m "test: PR feature"
git push
```

### 4. Check Backend Logs
Look for:
```
Risk assessment: LOW RISK
LOW RISK: Auto-committing directly to main branch
Successfully committed fix: abc123
```

## 🎨 Risk Levels

| Risk | Triggers | Action |
|------|----------|--------|
| **LOW** | Syntax errors, single file, high confidence | Auto-commit to main |
| **MEDIUM** | Config errors, 2-3 files, moderate confidence | Create PR |
| **HIGH** | Test failures, >3 files, critical files | Create PR with review |

## 🔍 What to Look For

### Low-Risk (Auto-Commit)
- ✅ Direct commit to main
- ✅ Commit message: "[CI Healer] ..."
- ✅ Pipeline re-runs automatically
- ❌ No PR created

### Medium/High-Risk (PR)
- ✅ New PR created
- ✅ Branch: `ci-healer/fix-{pipeline_id}`
- ✅ PR title: "[CI Healer] Fix: ..."
- ✅ Detailed description with risk level
- ❌ No direct commit to main

## 🚀 Test Different Risk Levels

### Test Low-Risk (Syntax Error)
```python
def test()  # Missing colon
    pass
```
**Expected:** Auto-commit

### Test Medium-Risk (Config Error)
```python
import os
api_key = os.environ['MISSING_VAR']  # Missing env var
```
**Expected:** PR created

### Test High-Risk (Multiple Files)
Create 4+ files with errors
**Expected:** PR created

## 📊 Why This Matters

**For Hackathon Judges:**
- Shows production-ready thinking
- Demonstrates risk management
- Enterprise-grade solution
- Not just a "toy" project

**For Real-World Use:**
- Companies trust it (safety net)
- Fast for simple fixes
- Careful with complex changes
- Meets compliance requirements

## 🎤 Demo Talking Points

1. **"Intelligent Risk Assessment"**
   - "Our system doesn't blindly auto-fix everything"
   - "It assesses risk and adapts its approach"

2. **"Speed + Safety"**
   - "Simple syntax errors? Fixed in 30 seconds"
   - "Complex logic changes? Creates PR for review"

3. **"Enterprise Ready"**
   - "This is what makes it production-ready"
   - "Companies need this safety net"

4. **"Competitive Advantage"**
   - "Most tools are all-or-nothing"
   - "We're intelligent about when to auto-fix"

## 🔧 Quick Troubleshooting

**No risk assessment logs?**
- Check backend is running
- Verify AUTO_FIX_ENABLED=true

**PR not created?**
- Check PyGithub installed
- Verify GitHub token permissions
- Check repository format: owner/repo

**Always auto-commits?**
- Check error type (syntax = low risk)
- Try config error for medium risk
- Try test failure for high risk

## 📈 Success Criteria

After testing, you should have:
- ✅ Seen risk assessment logs
- ✅ Low-risk auto-committed
- ✅ Medium/high-risk created PR
- ✅ PR description is detailed
- ✅ System works end-to-end

## 🎯 Next Steps

1. Test low-risk scenario (5 min)
2. Test medium-risk scenario (5 min)
3. Test high-risk scenario (5 min)
4. Review PR descriptions
5. Prepare demo script
6. Practice presentation

---

**The feature is ready. Time to test and demo! 🚀**
