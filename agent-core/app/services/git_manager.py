from typing import Dict, Any
from loguru import logger
import git
from pathlib import Path
import tempfile
import shutil

class GitManager:
    """Manages git operations for applying fixes"""
    
    def __init__(self):
        self.temp_repos = {}
    
    async def clone_repository(self, repo_url: str, branch: str) -> str:
        """Clone repository to temporary location"""
        try:
            temp_dir = tempfile.mkdtemp()
            logger.info(f"Cloning {repo_url} to {temp_dir}")
            
            # Use token authentication for GitHub
            from app.core.config import settings
            if settings.GITHUB_TOKEN and 'github.com' in repo_url:
                # Insert token into URL
                auth_url = repo_url.replace('https://', f'https://{settings.GITHUB_TOKEN}@')
                repo = git.Repo.clone_from(auth_url, temp_dir, branch=branch)
            else:
                repo = git.Repo.clone_from(repo_url, temp_dir, branch=branch)
            
            self.temp_repos[repo_url] = temp_dir
            
            return temp_dir
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return ""
    
    async def apply_changes(self, repo_path: str, changes: list) -> bool:
        """Apply fix changes to repository"""
        try:
            changes_applied = False
            
            # If no changes specified but this is a syntax error, try to find and fix Python files
            if not changes:
                logger.warning("No changes specified")
                return False
            
            for change in changes:
                # Extract just the filename from the file path
                file_name = change.get('file', '')
                if not file_name:
                    logger.warning(f"No file specified in change: {change}")
                    continue
                
                # The file path should already be relative to repo root from error analyzer
                file_path = Path(repo_path) / file_name
                
                logger.info(f"Attempting to apply change to: {file_name}")
                logger.info(f"Full path: {file_path}")
                logger.info(f"Action: {change['action']}")
                
                # Check if file exists
                if not file_path.exists():
                    logger.warning(f"File not found at expected path: {file_path}")
                    # Try to find the file in the repository
                    found_path = self._find_file_in_repo(repo_path, file_name)
                    if found_path:
                        file_path = found_path
                        logger.info(f"Found file at: {file_path}")
                    else:
                        logger.error(f"Could not locate file: {file_name} in repository")
                        continue
                else:
                    logger.info(f"File exists at expected path: {file_path}")
                
                if change['action'] == 'replace_entire_file':
                    result = await self._replace_entire_file(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully replaced entire file: {file_path}")
                    else:
                        logger.error(f"Failed to replace file: {file_path}")
                elif change['action'] == 'ai_fix_syntax':
                    result = await self._ai_fix_syntax_file(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully applied AI syntax fix to {file_path}")
                    else:
                        logger.error(f"Failed to apply AI syntax fix to {file_path}")
                elif change['action'] == 'add_missing_package':
                    result = await self._add_missing_package(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully added missing package to {file_path}")
                    else:
                        logger.error(f"Failed to add missing package to {file_path}")
                elif change['action'] == 'update_dependency':
                    await self._update_dependency_file(file_path, change)
                    changes_applied = True
                elif change['action'] == 'fix_syntax':
                    result = await self._fix_syntax_file(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully applied syntax fix to {file_path}")
                    else:
                        logger.warning(f"No syntax changes applied to {file_path}")
                elif change['action'] == 'update_config':
                    await self._update_config_file(file_path, change)
                    changes_applied = True
                elif change['action'] == 'add_env_var':
                    await self._add_env_var(file_path, change)
                    changes_applied = True
                elif change['action'] == 'fix_permissions':
                    result = await self._fix_permissions(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully fixed permissions for {file_path}")
                    else:
                        logger.error(f"Failed to fix permissions for {file_path}")
                elif change['action'] == 'fix_python_version':
                    result = await self._fix_python_version(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully fixed Python version in {file_path}")
                    else:
                        logger.error(f"Failed to fix Python version in {file_path}")
                elif change['action'] == 'fix_node_version':
                    result = await self._fix_node_version(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully fixed Node version in {file_path}")
                    else:
                        logger.error(f"Failed to fix Node version in {file_path}")
                elif change['action'] == 'add_env_vars':
                    result = await self._add_env_vars_to_workflow(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully added env vars to {file_path}")
                    else:
                        logger.error(f"Failed to add env vars to {file_path}")
                elif change['action'] == 'add_system_packages':
                    result = await self._add_system_packages(file_path, change)
                    if result:
                        changes_applied = True
                        logger.info(f"Successfully added system packages to {file_path}")
                    else:
                        logger.error(f"Failed to add system packages to {file_path}")
                else:
                    logger.warning(f"Unknown action: {change['action']}")
            
            logger.info(f"Changes applied: {changes_applied}")
            return changes_applied
        except Exception as e:
            logger.error(f"Failed to apply changes: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _find_file_in_repo(self, repo_path: str, filename: str) -> Path:
        """Search for a file in the repository with intelligent fallback"""
        repo_root = Path(repo_path)

        # Get just the base filename
        base_name = Path(filename).name

        logger.info(f"Searching for file: {filename} (base: {base_name})")

        # Strategy 1: Try exact path match
        exact_path = repo_root / filename
        if exact_path.exists() and exact_path.is_file():
            logger.info(f"Found exact match: {exact_path}")
            return exact_path

        # Strategy 2: Search for the file by name recursively
        logger.info(f"Searching recursively for: {base_name}")
        for file_path in repo_root.rglob(base_name):
            if file_path.is_file():
                # Exclude system directories
                if not any(part.startswith('.') or part in ['venv', 'node_modules', '__pycache__', 'dist', 'build'] 
                         for part in file_path.parts):
                    logger.info(f"Found {base_name} at {file_path}")
                    return file_path

        # Strategy 3: For Python files, find ANY .py file with syntax errors
        if base_name.endswith('.py') or filename.endswith('.py'):
            logger.info(f"Looking for Python files with potential syntax errors")
            python_files = []
            for file_path in repo_root.rglob('*.py'):
                if file_path.is_file():
                    # Exclude system files and directories
                    if not any(part.startswith('.') or part in ['venv', 'node_modules', '__pycache__', 'dist', 'build'] 
                             for part in file_path.parts):
                        if file_path.name != '__init__.py':
                            python_files.append(file_path)

            # Check each Python file for syntax errors
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Quick check for common syntax errors
                        if self._has_syntax_errors(content):
                            logger.info(f"Found Python file with syntax errors: {py_file}")
                            return py_file
                except Exception as e:
                    logger.debug(f"Could not check {py_file}: {e}")

            # If no files with syntax errors found, return the first Python file that's not a test/workflow file
            non_test_files = [f for f in python_files if 'test' not in f.name.lower() and 'workflow' not in str(f).lower()]
            if non_test_files:
                logger.info(f"No syntax errors detected, using first non-test Python file: {non_test_files[0]}")
                return non_test_files[0]
            
            # Last resort: return first Python file
            if python_files:
                logger.info(f"Using first Python file: {python_files[0]}")
                return python_files[0]

        # Strategy 4: For YAML/YML files, find workflow files
        if base_name.endswith(('.yml', '.yaml')) or filename.endswith(('.yml', '.yaml')):
            logger.info(f"Looking for workflow YAML files")
            for file_path in repo_root.rglob('*.yml'):
                if '.github/workflows' in str(file_path):
                    logger.info(f"Found workflow file: {file_path}")
                    return file_path
            for file_path in repo_root.rglob('*.yaml'):
                if '.github/workflows' in str(file_path):
                    logger.info(f"Found workflow file: {file_path}")
                    return file_path

        logger.warning(f"Could not find file: {filename}")
        return None

    def _has_syntax_errors(self, content: str) -> bool:
        """Quick check if Python code has obvious syntax errors"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Check for missing colons on def/class/if/for/while/try/except/with
            if stripped and not stripped.startswith('#'):
                if any(stripped.startswith(keyword) for keyword in ['def ', 'class ', 'if ', 'elif ', 'else', 'for ', 'while ', 'try', 'except', 'finally', 'with ']):
                    if not stripped.endswith(':') and not stripped.endswith('\\'):
                        return True
                
                # Check for unmatched parentheses, brackets, braces
                open_parens = stripped.count('(') - stripped.count(')')
                open_brackets = stripped.count('[') - stripped.count(']')
                open_braces = stripped.count('{') - stripped.count('}')
                
                if open_parens != 0 or open_brackets != 0 or open_braces != 0:
                    # If line doesn't end with a continuation character, it's likely an error
                    if not stripped.endswith(('\\', ',')):
                        return True
        
        return False


    
    async def commit_and_push(self, repo_path: str, message: str, 
                             author_name: str = "CI Healing Agent",
                             author_email: str = "agent@ci-healer.dev") -> str:
        """Commit changes and push to remote"""
        try:
            repo = git.Repo(repo_path)
            
            # Check if there are any changes
            if not repo.is_dirty() and not repo.untracked_files:
                logger.warning("No changes to commit")
                return ""
            
            # Stage all changes
            repo.git.add(A=True)
            
            # Commit
            repo.index.commit(
                message,
                author=git.Actor(author_name, author_email),
                committer=git.Actor(author_name, author_email)
            )
            
            # Push with token authentication
            from app.core.config import settings
            import os
            import subprocess
            
            if settings.GITHUB_TOKEN:
                # Get the original remote URL
                original_url = repo.remotes.origin.url
                logger.info(f"Original remote URL: {original_url[:50]}...")
                
                # Extract repo path from URL and clean it
                if 'github.com' in original_url:
                    # Remove any existing token from URL
                    clean_url = original_url
                    if '@github.com' in clean_url:
                        # URL already has authentication, extract the repo part
                        repo_part = clean_url.split('@github.com/')[-1]
                        clean_url = f'https://github.com/{repo_part}'
                    
                    # Remove trailing .git/ if present
                    clean_url = clean_url.rstrip('/')
                    
                    logger.info(f"Clean URL: {clean_url}")
                    
                    try:
                        # Method 1: Use subprocess with GIT_ASKPASS
                        env = os.environ.copy()
                        env['GIT_ASKPASS'] = 'echo'
                        env['GIT_USERNAME'] = settings.GITHUB_TOKEN
                        env['GIT_PASSWORD'] = ''
                        
                        # Set the clean URL
                        repo.remotes.origin.set_url(clean_url)
                        
                        # Try push with subprocess
                        result = subprocess.run(
                            ['git', 'push', 'origin', 'HEAD'],
                            cwd=repo_path,
                            env=env,
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            commit_sha = repo.head.commit.hexsha
                            logger.info(f"Successfully committed and pushed: {commit_sha}")
                            return commit_sha
                        else:
                            logger.error(f"Push failed (method 1): {result.stderr}")
                            
                            # Method 2: Try with token in URL
                            auth_url = clean_url.replace('https://github.com/', f'https://{settings.GITHUB_TOKEN}@github.com/')
                            repo.remotes.origin.set_url(auth_url)
                            
                            repo.git.push('origin', 'HEAD')
                            
                            # Restore clean URL
                            repo.remotes.origin.set_url(clean_url)
                            
                            commit_sha = repo.head.commit.hexsha
                            logger.info(f"Successfully committed and pushed (method 2): {commit_sha}")
                            return commit_sha
                        
                    except Exception as e:
                        logger.error(f"Push failed: {e}")
                        # Restore clean URL on error
                        try:
                            repo.remotes.origin.set_url(clean_url)
                        except:
                            pass
                        return ""
                else:
                    logger.error("Not a GitHub repository")
                    return ""
            else:
                logger.error("No GitHub token configured")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to commit and push: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""
    
    async def cleanup_repository(self, repo_url: str):
        """Clean up temporary repository"""
        if repo_url in self.temp_repos:
            temp_dir = self.temp_repos[repo_url]
            try:
                shutil.rmtree(temp_dir)
                del self.temp_repos[repo_url]
                logger.info(f"Cleaned up {temp_dir}")
            except Exception as e:
                logger.error(f"Failed to cleanup: {e}")
    
    async def _ai_fix_syntax_file(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Use AI to analyze and fix syntax errors in file"""
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            # Read the file content
            content = file_path.read_text(encoding='utf-8')
            logger.info(f"Read file {file_path} ({len(content)} characters)")
            
            # Get error details from change
            error_message = change.get('error_message', 'Syntax error detected')
            root_cause = change.get('root_cause', 'Unknown')
            error_category = change.get('error_category', 'unknown')
            
            # Use AI to fix the file
            from app.core.config import settings
            
            # Initialize AI client
            client = None
            ai_provider = settings.AI_PROVIDER.lower()
            
            if ai_provider == "groq":
                try:
                    from groq import Groq
                    client = Groq(api_key=settings.GROQ_API_KEY)
                except ImportError:
                    logger.error("Groq package not installed")
                    return False
            elif ai_provider == "openai":
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=settings.OPENAI_API_KEY)
                except ImportError:
                    logger.error("OpenAI package not installed")
                    return False
            else:
                logger.error(f"Unsupported AI provider: {ai_provider}")
                return False
            
            if not client:
                logger.error("AI client not initialized")
                return False
            
            # Create prompt for AI
            prompt = f"""You are a code fixing expert. A CI/CD pipeline failed and you need to fix this Python file.

File: {file_path.name}
Error Message: {error_message}
Root Cause: {root_cause}
Error Category: {error_category}

Here is the COMPLETE file content:

```python
{content}
```

Your task:
1. Analyze the ENTIRE file carefully
2. Look for ALL issues:
   - Missing imports (if code uses 'json', 'os', 'datetime', 'pd', 'np', etc. without importing)
   - Syntax errors (missing colons, parentheses, indentation issues)
   - Any other errors
3. Fix ALL issues found:
   - ADD missing import statements at the TOP of the file (after any existing imports)
   - FIX all syntax errors
   - Remove any comment lines that say "# Missing: import ..." - these are just notes, replace them with actual imports
4. Return the COMPLETE CORRECTED file with ALL errors fixed

CRITICAL RULES:
- If you see comments like "# Missing: import json", REMOVE the comment and ADD the actual import: "import json"
- If code uses 'json.loads', 'os.getenv', 'datetime.now', etc., you MUST add the imports
- Common imports: import json, import os, from datetime import datetime, import pandas as pd, import numpy as np
- Fix ALL syntax errors (missing colons on def/class/if/for/while/try)
- Return ONLY the corrected Python code, no explanations, no markdown
- The code must be complete and runnable"""

            logger.info(f"Sending file to AI for analysis ({ai_provider})...")
            logger.debug(f"Original file content:\n{content}")
            logger.debug(f"Prompt length: {len(prompt)} characters")
            
            # Call AI
            if ai_provider == "groq":
                response = client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a code fixing expert. Return only the corrected code, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
                logger.debug(f"AI response:\n{corrected_code}")
            elif ai_provider == "openai":
                response = client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a code fixing expert. Return only the corrected code, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
            else:
                return False
            
            # Clean up the response - remove markdown code blocks if present
            if '```python' in corrected_code:
                corrected_code = corrected_code.split('```python')[1].split('```')[0].strip()
            elif '```' in corrected_code:
                corrected_code = corrected_code.split('```')[1].split('```')[0].strip()
            
            logger.info(f"AI generated corrected code ({len(corrected_code)} characters)")
            
            # Only write if the code actually changed
            if corrected_code != content:
                file_path.write_text(corrected_code, encoding='utf-8')
                logger.info(f"Successfully replaced file with AI-corrected version")
                return True
            else:
                logger.warning(f"AI generated same code - no changes detected")
                return False
        
        except Exception as e:
            logger.error(f"Failed to AI-fix syntax in {file_path}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def _replace_entire_file(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Replace entire file content with AI-generated corrected code"""
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            # Get the corrected code from the change
            corrected_code = change.get('code_snippet', '')
            if not corrected_code:
                logger.error("No code_snippet provided in change")
                return False
            
            # Read original content for logging
            original_content = file_path.read_text(encoding='utf-8')
            logger.info(f"Original file size: {len(original_content)} characters")
            logger.info(f"Corrected file size: {len(corrected_code)} characters")
            
            # Write the corrected code
            file_path.write_text(corrected_code, encoding='utf-8')
            logger.info(f"Successfully replaced entire file: {file_path}")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to replace file {file_path}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def _update_dependency_file(self, file_path: Path, change: Dict[str, Any]):
        """Update dependency file (package.json, requirements.txt, etc.)"""
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return
        
        # Simplified: just add a comment for now
        # In production, parse and update specific dependencies
        content = file_path.read_text()
        file_path.write_text(content)  # Placeholder
    
    async def _fix_syntax_file(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Fix syntax in file"""
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            content = file_path.read_text()
            original_content = content
            
            # Apply code snippet if provided
            if 'code_snippet' in change and change['code_snippet']:
                # Replace the entire file with the fixed version
                file_path.write_text(change['code_snippet'])
                logger.info(f"Applied syntax fix to {file_path}")
                return True
            else:
                # Try basic Python syntax fixes
                if file_path.suffix == '.py':
                    fixed_content = self._auto_fix_python_syntax(content)
                    if fixed_content != content:
                        file_path.write_text(fixed_content)
                        logger.info(f"Auto-fixed Python syntax in {file_path}")
                        return True
                    else:
                        logger.info(f"No syntax fixes needed for {file_path}")
                        return False
                else:
                    logger.info(f"No auto-fix available for {file_path.suffix} files")
                    return False
        except Exception as e:
            logger.error(f"Failed to fix syntax in {file_path}: {e}")
            return False
    
    def _auto_fix_python_syntax(self, content: str) -> str:
        """Attempt to auto-fix common Python syntax errors"""
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            fixed_line = line
            
            # Fix missing colons in function/class definitions
            if line.strip().startswith(('def ', 'class ', 'if ', 'elif ', 'else', 'for ', 'while ', 'try', 'except', 'finally')):
                if not line.rstrip().endswith(':') and not line.rstrip().endswith('\\'):
                    # Check if it's a complete statement
                    stripped = line.strip()
                    if stripped and not stripped.endswith(':'):
                        # Handle comments - insert colon before comment
                        if '#' in stripped:
                            # Find the comment position
                            comment_pos = stripped.find('#')
                            code_part = stripped[:comment_pos].rstrip()
                            comment_part = stripped[comment_pos:]
                            
                            # For function/class definitions, add colon after closing parenthesis
                            if stripped.startswith(('def ', 'class ')) and ')' in code_part:
                                # Find last closing parenthesis
                                last_paren = code_part.rfind(')')
                                fixed_code = code_part[:last_paren+1] + ':'
                                indent = len(line) - len(line.lstrip())
                                fixed_line = ' ' * indent + fixed_code + '  ' + comment_part
                                logger.debug(f"Added missing colon after ) on line {i+1}")
                            else:
                                # Add colon after code, before comment
                                indent = len(line) - len(line.lstrip())
                                fixed_line = ' ' * indent + code_part + ':  ' + comment_part
                                logger.debug(f"Added missing colon before comment on line {i+1}")
                        else:
                            # No comment, add colon at end
                            indent = len(line) - len(line.lstrip())
                            fixed_line = ' ' * indent + stripped + ':'
                            logger.debug(f"Added missing colon to line {i+1}")
            
            # Fix missing closing parentheses/brackets (basic)
            open_parens = fixed_line.count('(') - fixed_line.count(')')
            open_brackets = fixed_line.count('[') - fixed_line.count(']')
            open_braces = fixed_line.count('{') - fixed_line.count('}')
            
            if open_parens > 0:
                fixed_line += ')' * open_parens
            if open_brackets > 0:
                fixed_line += ']' * open_brackets
            if open_braces > 0:
                fixed_line += '}' * open_braces
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines)
    
    async def _update_config_file(self, file_path: Path, change: Dict[str, Any]):
        """Update configuration file"""
        if not file_path.exists():
            return
        
        content = file_path.read_text()
        file_path.write_text(content)
    
    async def _add_env_var(self, file_path: Path, change: Dict[str, Any]):
        """Add environment variable"""
        if not file_path.exists():
            file_path.touch()
        
        # Placeholder: Add env var
        content = file_path.read_text() if file_path.exists() else ""
        file_path.write_text(content)
    
    async def _add_missing_package(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Add missing package to requirements.txt using AI"""
        try:
            # Extract package name from error message
            error_message = change.get('error_message', '')
            logger.info(f"Analyzing error to find missing package: {error_message}")
            
            # Use AI to determine the correct package name and version
            from app.core.config import settings
            
            # Initialize AI client
            client = None
            ai_provider = settings.AI_PROVIDER.lower()
            
            if ai_provider == "groq":
                try:
                    from groq import Groq
                    client = Groq(api_key=settings.GROQ_API_KEY)
                except ImportError:
                    logger.error("Groq package not installed")
                    return False
            elif ai_provider == "openai":
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=settings.OPENAI_API_KEY)
                except ImportError:
                    logger.error("OpenAI package not installed")
                    return False
            else:
                logger.error(f"Unsupported AI provider: {ai_provider}")
                return False
            
            if not client:
                logger.error("AI client not initialized")
                return False
            
            # Read current requirements.txt if it exists
            current_requirements = ""
            if file_path.exists():
                current_requirements = file_path.read_text(encoding='utf-8')
                logger.info(f"Current requirements.txt:\n{current_requirements}")
            else:
                logger.info("requirements.txt does not exist, will create it")
            
            # Create prompt for AI
            prompt = f"""You are a Python dependency expert. A CI/CD pipeline failed with this error:

Error: {error_message}

Current requirements.txt:
```
{current_requirements if current_requirements else "# Empty file"}
```

Your task:
1. Identify the missing Python package from the error message
2. Determine the correct package name to install (e.g., "beautifulsoup4" for "bs4", "pillow" for "PIL")
3. Find a stable, recent version number
4. Add it to requirements.txt

IMPORTANT RULES:
- For "ModuleNotFoundError: No module named 'matplotlib'", add: matplotlib==3.8.0
- For "ModuleNotFoundError: No module named 'bs4'", add: beautifulsoup4==4.12.0
- For "ModuleNotFoundError: No module named 'PIL'", add: Pillow==10.0.0
- For "ModuleNotFoundError: No module named 'cv2'", add: opencv-python==4.8.0
- Use the INSTALL name, not the import name
- Use recent stable versions (2023-2024)
- Add the package at the end of the file
- Return ONLY the complete updated requirements.txt content
- Do not add explanations or comments about what you added"""

            logger.info(f"Sending to AI for package analysis...")
            
            # Call AI
            if ai_provider == "groq":
                response = client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a Python dependency expert. Return only the updated requirements.txt content, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.1
                )
                updated_requirements = response.choices[0].message.content.strip()
            elif ai_provider == "openai":
                response = client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a Python dependency expert. Return only the updated requirements.txt content, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.1
                )
                updated_requirements = response.choices[0].message.content.strip()
            else:
                return False
            
            # Clean up the response - remove markdown code blocks if present
            if '```' in updated_requirements:
                # Extract content between code blocks
                parts = updated_requirements.split('```')
                for part in parts:
                    if part.strip() and not part.strip().startswith(('txt', 'text', 'python')):
                        updated_requirements = part.strip()
                        break
            
            logger.info(f"AI generated updated requirements.txt ({len(updated_requirements)} characters)")
            logger.debug(f"Updated requirements:\n{updated_requirements}")
            
            # Only write if content actually changed
            if updated_requirements != current_requirements:
                # Ensure parent directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the updated requirements
                file_path.write_text(updated_requirements, encoding='utf-8')
                logger.info(f"Successfully updated requirements.txt with missing package")
                return True
            else:
                logger.warning(f"AI generated same requirements.txt - no changes detected")
                return False
        
        except Exception as e:
            logger.error(f"Failed to add missing package to {file_path}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    async def _fix_permissions(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Fix file permissions (add executable permissions)"""
        try:
            import stat
            import os
            
            logger.info(f"Fixing permissions for {file_path}")
            
            # Add executable permissions (chmod +x equivalent)
            current_permissions = os.stat(file_path).st_mode
            new_permissions = current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            
            os.chmod(file_path, new_permissions)
            logger.info(f"Successfully added executable permissions to {file_path}")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to fix permissions for {file_path}: {e}")
            return False

    async def _fix_python_version(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Fix Python version mismatch in GitHub Actions workflow"""
        try:
            logger.info(f"Fixing Python version in {file_path}")
            
            # Read workflow file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use AI to fix Python version
            prompt = f"""Fix the Python version in this GitHub Actions workflow file.

Error: {change.get('error_message', 'Python version mismatch')}
Root Cause: {change.get('root_cause', 'Python version in CI differs from requirements')}

Current workflow file:
```yaml
{content}
```

Instructions:
1. Identify the Python version being used (look for python-version or setup-python)
2. Update it to a compatible version (prefer 3.11 or 3.12 for modern projects)
3. If there's a version constraint in requirements, match it
4. Return the COMPLETE corrected workflow file

Return ONLY the corrected YAML, no explanations."""

            if not self.client:
                logger.error("No AI client available")
                return False
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are a DevOps expert. Return only corrected YAML."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            corrected_content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks
            if '```yaml' in corrected_content:
                corrected_content = corrected_content.split('```yaml')[1].split('```')[0].strip()
            elif '```' in corrected_content:
                corrected_content = corrected_content.split('```')[1].split('```')[0].strip()
            
            # Check if content changed
            if corrected_content == content:
                logger.warning("AI generated same content - no changes needed")
                return False
            
            # Write corrected content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            
            logger.info(f"Successfully fixed Python version in {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to fix Python version: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def _fix_node_version(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Fix Node.js version mismatch in GitHub Actions workflow"""
        try:
            logger.info(f"Fixing Node version in {file_path}")
            
            # Read workflow file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use AI to fix Node version
            prompt = f"""Fix the Node.js version in this GitHub Actions workflow file.

Error: {change.get('error_message', 'Node version mismatch')}
Root Cause: {change.get('root_cause', 'Node version in CI differs from requirements')}

Current workflow file:
```yaml
{content}
```

Instructions:
1. Identify the Node version being used (look for node-version or setup-node)
2. Update it to a compatible version (prefer 18.x or 20.x for modern projects)
3. If there's a version in package.json engines, match it
4. Return the COMPLETE corrected workflow file

Return ONLY the corrected YAML, no explanations."""

            if not self.client:
                logger.error("No AI client available")
                return False
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are a DevOps expert. Return only corrected YAML."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            corrected_content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks
            if '```yaml' in corrected_content:
                corrected_content = corrected_content.split('```yaml')[1].split('```')[0].strip()
            elif '```' in corrected_content:
                corrected_content = corrected_content.split('```')[1].split('```')[0].strip()
            
            # Check if content changed
            if corrected_content == content:
                logger.warning("AI generated same content - no changes needed")
                return False
            
            # Write corrected content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            
            logger.info(f"Successfully fixed Node version in {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to fix Node version: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def _add_env_vars_to_workflow(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Add missing environment variables to GitHub Actions workflow"""
        try:
            logger.info(f"Adding environment variables to {file_path}")
            
            # Read workflow file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use AI to add env vars
            prompt = f"""Add missing environment variables to this GitHub Actions workflow file.

Error: {change.get('error_message', 'Missing environment variable')}
Root Cause: {change.get('root_cause', 'Environment variables not set in CI')}

Current workflow file:
```yaml
{content}
```

Instructions:
1. Identify which environment variable is missing from the error message
2. Add it to the workflow under 'env:' section
3. Use GitHub Secrets syntax: ${{{{ secrets.VARIABLE_NAME }}}}
4. If no env section exists, create one
5. Return the COMPLETE corrected workflow file

Return ONLY the corrected YAML, no explanations."""

            if not self.client:
                logger.error("No AI client available")
                return False
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are a DevOps expert. Return only corrected YAML."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            corrected_content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks
            if '```yaml' in corrected_content:
                corrected_content = corrected_content.split('```yaml')[1].split('```')[0].strip()
            elif '```' in corrected_content:
                corrected_content = corrected_content.split('```')[1].split('```')[0].strip()
            
            # Check if content changed
            if corrected_content == content:
                logger.warning("AI generated same content - no changes needed")
                return False
            
            # Write corrected content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            
            logger.info(f"Successfully added env vars to {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to add env vars: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    async def _add_system_packages(self, file_path: Path, change: Dict[str, Any]) -> bool:
        """Add missing system packages to GitHub Actions workflow"""
        try:
            logger.info(f"Adding system packages to {file_path}")
            
            # Read workflow file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use AI to add system packages
            prompt = f"""Add missing system packages to this GitHub Actions workflow file.

Error: {change.get('error_message', 'Command not found')}
Root Cause: {change.get('root_cause', 'System dependencies not installed in CI')}

Current workflow file:
```yaml
{content}
```

Instructions:
1. Identify which command/library is missing from the error message
2. Add a step to install it using apt-get (for Ubuntu runners)
3. Common packages: build-essential, libpq-dev, python3-dev, etc.
4. Add the step BEFORE the step that uses the command
5. Return the COMPLETE corrected workflow file

Example step to add:
```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y <package-name>
```

Return ONLY the corrected YAML, no explanations."""

            if not self.client:
                logger.error("No AI client available")
                return False
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are a DevOps expert. Return only corrected YAML."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            corrected_content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks
            if '```yaml' in corrected_content:
                corrected_content = corrected_content.split('```yaml')[1].split('```')[0].strip()
            elif '```' in corrected_content:
                corrected_content = corrected_content.split('```')[1].split('```')[0].strip()
            
            # Check if content changed
            if corrected_content == content:
                logger.warning("AI generated same content - no changes needed")
                return False
            
            # Write corrected content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            
            logger.info(f"Successfully added system packages to {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to add system packages: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
