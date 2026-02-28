from typing import Dict, Any, List
from loguru import logger
from app.models.pipeline import ErrorCategory
from app.core.config import settings
import json

class FixEngine:
    """Automated fix generation engine"""
    
    def __init__(self):
        self.client = None
        self.ai_provider = settings.AI_PROVIDER.lower()
        
        if self.ai_provider == "openai" and settings.OPENAI_API_KEY:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.ai_provider == "ollama":
            try:
                import ollama
                self.client = ollama
                logger.info(f"Ollama client initialized for fix generation")
            except ImportError:
                logger.warning("Ollama package not installed")
                self.client = None
        elif self.ai_provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info(f"Groq client initialized for fix generation")
            except ImportError:
                logger.warning("Groq package not installed")
                self.client = None
        elif self.ai_provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.client = genai
                logger.info(f"Gemini client initialized for fix generation")
            except ImportError:
                logger.warning("Google Generative AI package not installed")
                self.client = None
    
    async def generate_fix(self, analysis: Dict[str, Any], 
                          repository_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automated fix based on error analysis"""
        
        category = analysis['error_category']
        
        # Route to appropriate fix strategy
        if category == ErrorCategory.DEPENDENCY_CONFLICT:
            return await self._fix_dependency_conflict(analysis, repository_context)
        elif category == ErrorCategory.TEST_FAILURE:
            return await self._fix_test_failure(analysis, repository_context)
        elif category == ErrorCategory.SYNTAX_ERROR:
            return await self._fix_syntax_error(analysis, repository_context)
        elif category == ErrorCategory.CONFIGURATION_ERROR:
            return await self._fix_configuration_error(analysis, repository_context)
        elif category == ErrorCategory.ENVIRONMENT_ISSUE:
            return await self._fix_environment_issue(analysis, repository_context)
        else:
            return await self._generic_fix(analysis, repository_context)
    
    async def _fix_dependency_conflict(self, analysis: Dict[str, Any], 
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix dependency conflicts"""
        
        # Example fix strategies
        changes = []
        
        # Strategy 1: Update package versions
        if 'package.json' in str(analysis.get('affected_files', [])):
            changes.append({
                'file': 'package.json',
                'action': 'update_dependency',
                'description': 'Update conflicting package versions'
            })
        
        # Strategy 2: Update requirements.txt
        if 'requirements.txt' in str(analysis.get('affected_files', [])):
            changes.append({
                'file': 'requirements.txt',
                'action': 'pin_version',
                'description': 'Pin dependency versions to resolve conflict'
            })
        
        # Use AI for specific fix if available
        if self.client:
            ai_fix = await self._ai_generate_fix(analysis, context)
            if ai_fix:
                changes.extend(ai_fix.get('changes', []))
        
        return {
            'fix_type': 'dependency_conflict_resolution',
            'description': 'Resolved dependency version conflicts',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _fix_test_failure(self, analysis: Dict[str, Any], 
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix test failures"""
        
        changes = []
        
        # Identify test files
        test_files = [f for f in analysis.get('affected_files', []) 
                     if 'test' in f.lower() or 'spec' in f.lower()]
        
        for test_file in test_files:
            changes.append({
                'file': test_file,
                'action': 'update_test',
                'description': 'Update test assertions or mocks'
            })
        
        return {
            'fix_type': 'test_failure_fix',
            'description': 'Fixed failing test cases',
            'changes': changes,
            'auto_applicable': False  # Tests need manual review
        }
    
    async def _fix_syntax_error(self, analysis: Dict[str, Any], 
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix syntax errors"""
        
        changes = []
        
        for file in analysis.get('affected_files', []):
            changes.append({
                'file': file,
                'action': 'fix_syntax',
                'description': 'Auto-format and fix syntax issues'
            })
        
        return {
            'fix_type': 'syntax_error_fix',
            'description': 'Fixed syntax errors',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _fix_configuration_error(self, analysis: Dict[str, Any], 
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix configuration errors"""
        
        changes = []
        
        config_files = [f for f in analysis.get('affected_files', [])
                       if any(ext in f for ext in ['.yaml', '.yml', '.json', '.toml', '.ini'])]
        
        for config_file in config_files:
            changes.append({
                'file': config_file,
                'action': 'update_config',
                'description': 'Fix configuration syntax or add missing keys'
            })
        
        return {
            'fix_type': 'configuration_fix',
            'description': 'Fixed configuration errors',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _fix_environment_issue(self, analysis: Dict[str, Any], 
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix environment issues"""
        
        changes = [{
            'file': '.env.example',
            'action': 'add_env_var',
            'description': 'Add missing environment variables'
        }]
        
        return {
            'fix_type': 'environment_fix',
            'description': 'Fixed environment configuration',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _generic_fix(self, analysis: Dict[str, Any], 
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Generic fix for unknown errors"""
        
        return {
            'fix_type': 'generic_fix',
            'description': 'Attempted generic error resolution',
            'changes': [],
            'auto_applicable': False
        }
    
    async def _ai_generate_fix(self, analysis: Dict[str, Any], 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to generate specific fix"""
        
        if not self.client:
            return {}
            
        try:
            prompt = f"""Generate a specific fix for this CI/CD failure:

Error Category: {analysis['error_category']}
Error Message: {analysis['error_message']}
Root Cause: {analysis.get('root_cause', 'Unknown')}
Affected Files: {', '.join(analysis.get('affected_files', [])[:5])}

Provide a JSON response with:
{{
  "changes": [
    {{
      "file": "path/to/file",
      "action": "specific_action",
      "description": "what to change",
      "code_snippet": "actual code change if applicable"
    }}
  ]
}}

Keep it practical and executable."""

            if self.ai_provider == "ollama":
                response = self.client.chat(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD fix automation expert. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response['message']['content'].strip()
                
            elif self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD fix automation expert. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.2
                )
                content = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "groq":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD fix automation expert. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.2
                )
                content = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "gemini":
                model = self.client.GenerativeModel(settings.AI_MODEL)
                full_prompt = "You are a CI/CD fix automation expert. Respond only with valid JSON.\n\n" + prompt
                response = model.generate_content(full_prompt)
                content = response.text.strip()
                
            elif self.ai_provider == "anthropic":
                response = self.client.messages.create(
                    model=settings.AI_MODEL,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.content[0].text.strip()
            else:
                return {}
            
            # Extract JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            return json.loads(content)
        
        except Exception as e:
            logger.error(f"AI fix generation failed: {e}")
            return {}
