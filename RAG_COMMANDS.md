# RAG Testing - Quick Command Reference

## 🚀 Quick Start (3 Commands)

### 1. Test RAG Installation
```bash
python test_rag_quick.py
```
**What it does:** Tests RAG imports, initialization, storage, and retrieval  
**Time:** 1-2 minutes (first run), 10 seconds (subsequent runs)  
**Expected:** All 5 tests pass with ✅

---

### 2. Start the Backend
```bash
cd agent-core
python main.py
```
**What to look for:**
```
INFO | RAG service initialized with 0 stored fixes
INFO | Groq client initialized
INFO | Starting pipeline monitoring...
```

---

### 3. Check RAG Statistics
```bash
curl http://localhost:8000/api/rag/statistics
```
**Expected output:**
```json
{
  "status": "success",
  "data": {
    "enabled": true,
    "total_fixes": 0,
    "categories": {}
  }
}
```

---

## 📊 Monitoring Commands

### Check RAG Status
```bash
curl http://localhost:8000/api/rag/statistics
```

### Watch RAG Statistics (Auto-refresh every 5 seconds)
```bash
# Windows PowerShell
while ($true) { curl http://localhost:8000/api/rag/statistics; Start-Sleep 5; Clear-Host }

# Linux/Mac
watch -n 5 'curl -s http://localhost:8000/api/rag/statistics | jq'
```

### Check RAG Data Directory
```bash
ls -la agent-core/rag_data/
```

### Clear RAG Knowledge Base (if needed)
```bash
curl -X POST http://localhost:8000/api/rag/clear
```

---

## 🧪 Testing Workflow

### Complete Test (15 minutes)

**Terminal 1 - Backend:**
```bash
cd agent-core
python main.py
```

**Terminal 2 - Monitoring:**
```bash
# Check initial state
curl http://localhost:8000/api/rag/statistics

# Create test error in sample_file_ci_cd
cd sample_file_ci_cd
echo "def test()
    print('missing colon')" > test_rag_1.py
git add test_rag_1.py
git commit -m "Test RAG: syntax error 1"
git push origin main

# Wait 30-60 seconds, then check RAG
curl http://localhost:8000/api/rag/statistics
# Should show: total_fixes: 1

# Create similar error
echo "def test2()
    print('another missing colon')" > test_rag_2.py
git add test_rag_2.py
git commit -m "Test RAG: syntax error 2"
git push origin main

# Wait 30-60 seconds, check logs for:
# "RAG: Found 1 similar fix to learn from"

# Check final statistics
curl http://localhost:8000/api/rag/statistics
# Should show: total_fixes: 2
```

---

## 🔍 Log Patterns to Look For

### RAG Initialization
```
INFO | RAG service initialized with X stored fixes
```

### No Similar Fixes (First Time)
```
INFO | RAG: No similar fixes found in knowledge base
```

### Similar Fixes Found (Learning!)
```
INFO | RAG: Found 3 similar fixes to learn from
INFO | RAG: Similarity: 95.3%, 87.2%, 72.1%
```

### Fix Stored Successfully
```
INFO | RAG: Successfully stored fix for future learning
```

---

## 📈 Expected Progression

### After 1st Fix:
```bash
curl http://localhost:8000/api/rag/statistics
```
```json
{
  "total_fixes": 1,
  "categories": {
    "syntax_error": 1
  }
}
```

### After 2nd Similar Fix:
```json
{
  "total_fixes": 2,
  "categories": {
    "syntax_error": 2
  }
}
```

### After Multiple Different Fixes:
```json
{
  "total_fixes": 5,
  "categories": {
    "syntax_error": 2,
    "dependency_conflict": 2,
    "environment_issue": 1
  }
}
```

---

## 🎯 Success Checklist

- [ ] `python test_rag_quick.py` passes all 5 tests
- [ ] Backend starts with "RAG service initialized"
- [ ] Statistics API returns `enabled: true`
- [ ] First fix shows "No similar fixes found"
- [ ] First fix shows "Successfully stored fix"
- [ ] Statistics show `total_fixes: 1`
- [ ] Second similar fix shows "Found 1 similar fix"
- [ ] Statistics show `total_fixes: 2`
- [ ] `agent-core/rag_data/` directory exists with files

---

## 🚨 Quick Troubleshooting

### RAG not enabled?
```bash
cd agent-core
pip install langchain langchain-community chromadb sentence-transformers tiktoken
```

### Slow first startup?
**Normal!** Downloading sentence-transformers model (~90MB, one-time)

### No similar fixes found?
**Check:**
1. Are fixes succeeding? (Check logs for "Successfully committed")
2. Are errors similar enough? (Need 70%+ similarity)
3. Is RAG storing fixes? (Check statistics after each fix)

### Clear and restart?
```bash
# Clear RAG knowledge base
curl -X POST http://localhost:8000/api/rag/clear

# Or delete data directory
rm -rf agent-core/rag_data/

# Restart backend
cd agent-core
python main.py
```

---

## 📚 Full Documentation

- **Detailed Testing:** `RAG_TEST_GUIDE.md`
- **Implementation Details:** `RAG_IMPLEMENTATION.md`
- **Setup Guide:** `RAG_SETUP_GUIDE.md`

---

**Quick Test:** `python test_rag_quick.py` (1-2 minutes)  
**Full Test:** See `RAG_TEST_GUIDE.md` (15 minutes)  
**Status:** ✅ Ready to Test
