#!/usr/bin/env python3
"""
Quick RAG Test Script
Tests RAG functionality without running the full system
"""

import sys
import os

# Add agent-core to path
sys.path.insert(0, 'agent-core')

print("=" * 80)
print("RAG QUICK TEST")
print("=" * 80)

# Test 1: Import RAG service
print("\n[1/5] Testing RAG imports...")
try:
    from app.services.rag_service import get_rag_service
    print("✅ RAG service imported successfully")
except ImportError as e:
    print(f"❌ Failed to import RAG service: {e}")
    print("\nInstall dependencies:")
    print("  cd agent-core")
    print("  pip install langchain langchain-community chromadb sentence-transformers tiktoken")
    sys.exit(1)

# Test 2: Initialize RAG
print("\n[2/5] Initializing RAG service...")
print("⏳ This may take 1-2 minutes on first run (downloading model)...")
try:
    rag = get_rag_service()
    if rag.enabled:
        print("✅ RAG service initialized successfully")
    else:
        print("❌ RAG service is disabled")
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed to initialize RAG: {e}")
    sys.exit(1)

# Test 3: Get statistics
print("\n[3/5] Getting RAG statistics...")
try:
    stats = rag.get_fix_statistics()
    print(f"✅ RAG Statistics:")
    print(f"   - Enabled: {stats.get('enabled')}")
    print(f"   - Total Fixes: {stats.get('total_fixes', 0)}")
    print(f"   - Categories: {stats.get('categories', {})}")
    print(f"   - Storage: {stats.get('persist_directory')}")
except Exception as e:
    print(f"❌ Failed to get statistics: {e}")
    sys.exit(1)

# Test 4: Store a test fix
print("\n[4/5] Storing a test fix...")
try:
    success = rag.store_successful_fix(
        error_category="syntax_error",
        error_message="SyntaxError: invalid syntax (missing colon)",
        root_cause="Missing colon after function definition",
        affected_files=["test.py"],
        fix_description="Added missing colon after function definition",
        fix_changes=[{
            "file": "test.py",
            "action": "fix_syntax",
            "description": "Added colon after def statement"
        }],
        confidence_score=95.0,
        repository="test/repo",
        success=True
    )
    
    if success:
        print("✅ Test fix stored successfully")
    else:
        print("⚠️  Fix storage returned False (may be disabled)")
except Exception as e:
    print(f"❌ Failed to store fix: {e}")
    sys.exit(1)

# Test 5: Retrieve similar fixes
print("\n[5/5] Retrieving similar fixes...")
try:
    similar = rag.retrieve_similar_fixes(
        error_category="syntax_error",
        error_message="SyntaxError: invalid syntax (missing colon)",
        root_cause="Missing colon in function",
        affected_files=["another_test.py"],
        top_k=3,
        similarity_threshold=0.7
    )
    
    if similar:
        print(f"✅ Found {len(similar)} similar fix(es):")
        for i, fix in enumerate(similar, 1):
            print(f"   {i}. Similarity: {fix['similarity']*100:.1f}%")
            print(f"      Description: {fix['fix_description']}")
    else:
        print("⚠️  No similar fixes found (this is normal if RAG is empty)")
except Exception as e:
    print(f"❌ Failed to retrieve fixes: {e}")
    sys.exit(1)

# Final statistics
print("\n" + "=" * 80)
print("FINAL RAG STATISTICS")
print("=" * 80)
try:
    final_stats = rag.get_fix_statistics()
    print(f"Total Fixes Stored: {final_stats.get('total_fixes', 0)}")
    print(f"Categories: {final_stats.get('categories', {})}")
    print(f"Storage Location: {final_stats.get('persist_directory')}")
except Exception as e:
    print(f"Error getting final stats: {e}")

print("\n" + "=" * 80)
print("✅ RAG TEST COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\nRAG is ready to use!")
print("\nNext steps:")
print("1. Start the backend: cd agent-core && python main.py")
print("2. Trigger a pipeline failure in your test repo")
print("3. Watch the logs for 'RAG: Successfully stored fix'")
print("4. Trigger a similar error and see 'RAG: Found X similar fixes'")
print("\nFor detailed testing guide, see: RAG_TEST_GUIDE.md")
