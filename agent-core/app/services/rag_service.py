"""
RAG (Retrieval-Augmented Generation) Service
Learns from past successful fixes to improve future fix accuracy
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime
import json
import hashlib
from pathlib import Path

try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not available. RAG features will be limited.")
    LANGCHAIN_AVAILABLE = False


class RAGService:
    """
    Production-ready RAG service for CI/CD fix learning
    
    Features:
    - Stores successful fixes in vector database
    - Retrieves similar past fixes for new errors
    - Learns from experience to improve accuracy
    - Persistent storage across restarts
    """
    
    def __init__(self, persist_directory: str = "agent-core/rag_data"):
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.embeddings = None
        self.enabled = LANGCHAIN_AVAILABLE
        
        if self.enabled:
            self._initialize_vectorstore()
        else:
            logger.warning("RAG service disabled - LangChain dependencies not available")
    
    def _initialize_vectorstore(self):
        """Initialize vector store with embeddings"""
        try:
            # Use sentence-transformers for embeddings (free, no API key needed)
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",  # Fast, accurate, 384 dimensions
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Initialize Chroma vector store
            Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
            
            self.vectorstore = Chroma(
                collection_name="fix_history",
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            logger.info(f"RAG service initialized with {self._get_fix_count()} stored fixes")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
            self.enabled = False
    
    def store_successful_fix(
        self,
        error_category: str,
        error_message: str,
        root_cause: str,
        affected_files: List[str],
        fix_description: str,
        fix_changes: List[Dict[str, Any]],
        confidence_score: float,
        repository: str,
        success: bool = True
    ) -> bool:
        """
        Store a successful fix in the knowledge base
        
        Args:
            error_category: Type of error (syntax, dependency, etc.)
            error_message: The error message from logs
            root_cause: Identified root cause
            affected_files: Files that were changed
            fix_description: Description of the fix
            fix_changes: Actual changes made
            confidence_score: Confidence in the fix
            repository: Repository where fix was applied
            success: Whether the fix was successful
        
        Returns:
            bool: True if stored successfully
        """
        if not self.enabled or not success:
            return False
        
        try:
            # Create a unique ID for this fix
            fix_id = self._generate_fix_id(error_message, repository)
            
            # Create comprehensive document text for embedding
            doc_text = self._create_document_text(
                error_category, error_message, root_cause,
                affected_files, fix_description, fix_changes
            )
            
            # Create metadata for filtering and retrieval
            metadata = {
                "fix_id": fix_id,
                "error_category": error_category,
                "repository": repository,
                "confidence_score": confidence_score,
                "timestamp": datetime.now().isoformat(),
                "affected_files": json.dumps(affected_files),
                "fix_description": fix_description,
                "fix_changes": json.dumps(fix_changes),
                "success": success
            }
            
            # Store in vector database
            document = Document(
                page_content=doc_text,
                metadata=metadata
            )
            
            self.vectorstore.add_documents([document])
            self.vectorstore.persist()
            
            logger.info(f"Stored successful fix in RAG: {fix_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store fix in RAG: {e}")
            return False
    
    def retrieve_similar_fixes(
        self,
        error_category: str,
        error_message: str,
        root_cause: str,
        affected_files: List[str],
        top_k: int = 3,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Retrieve similar past fixes for a new error
        
        Args:
            error_category: Type of error
            error_message: Current error message
            root_cause: Identified root cause
            affected_files: Files affected
            top_k: Number of similar fixes to retrieve
            similarity_threshold: Minimum similarity score (0-1)
        
        Returns:
            List of similar fixes with metadata
        """
        if not self.enabled:
            return []
        
        try:
            # Create query text
            query_text = self._create_query_text(
                error_category, error_message, root_cause, affected_files
            )
            
            # Search vector store
            results = self.vectorstore.similarity_search_with_score(
                query_text,
                k=top_k,
                filter={"error_category": error_category}  # Filter by category
            )
            
            # Filter by similarity threshold and format results
            similar_fixes = []
            for doc, score in results:
                # Convert distance to similarity (Chroma uses L2 distance)
                similarity = 1 / (1 + score)
                
                if similarity >= similarity_threshold:
                    similar_fixes.append({
                        "similarity": similarity,
                        "fix_description": doc.metadata.get("fix_description"),
                        "fix_changes": json.loads(doc.metadata.get("fix_changes", "[]")),
                        "confidence_score": doc.metadata.get("confidence_score"),
                        "repository": doc.metadata.get("repository"),
                        "timestamp": doc.metadata.get("timestamp"),
                        "affected_files": json.loads(doc.metadata.get("affected_files", "[]"))
                    })
            
            if similar_fixes:
                logger.info(f"Retrieved {len(similar_fixes)} similar fixes from RAG (similarity >= {similarity_threshold})")
            else:
                logger.info("No similar fixes found in RAG knowledge base")
            
            return similar_fixes
            
        except Exception as e:
            logger.error(f"Failed to retrieve similar fixes: {e}")
            return []
    
    def get_fix_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored fixes"""
        if not self.enabled:
            return {"enabled": False}
        
        try:
            total_fixes = self._get_fix_count()
            
            # Get category distribution
            categories = {}
            if total_fixes > 0:
                # Sample some documents to get category distribution
                sample_docs = self.vectorstore.get()
                for metadata in sample_docs.get('metadatas', []):
                    category = metadata.get('error_category', 'unknown')
                    categories[category] = categories.get(category, 0) + 1
            
            return {
                "enabled": True,
                "total_fixes": total_fixes,
                "categories": categories,
                "persist_directory": self.persist_directory
            }
            
        except Exception as e:
            logger.error(f"Failed to get fix statistics: {e}")
            return {"enabled": True, "error": str(e)}
    
    def _create_document_text(
        self,
        error_category: str,
        error_message: str,
        root_cause: str,
        affected_files: List[str],
        fix_description: str,
        fix_changes: List[Dict[str, Any]]
    ) -> str:
        """Create comprehensive text for embedding"""
        
        # Extract key information from changes
        change_summary = []
        for change in fix_changes:
            action = change.get('action', 'unknown')
            file = change.get('file', 'unknown')
            desc = change.get('description', '')
            change_summary.append(f"{action} in {file}: {desc}")
        
        # Create structured text
        text = f"""
Error Category: {error_category}
Error Message: {error_message}
Root Cause: {root_cause}
Affected Files: {', '.join(affected_files)}
Fix Description: {fix_description}
Changes Made: {'; '.join(change_summary)}
        """.strip()
        
        return text
    
    def _create_query_text(
        self,
        error_category: str,
        error_message: str,
        root_cause: str,
        affected_files: List[str]
    ) -> str:
        """Create query text for similarity search"""
        
        text = f"""
Error Category: {error_category}
Error Message: {error_message}
Root Cause: {root_cause}
Affected Files: {', '.join(affected_files)}
        """.strip()
        
        return text
    
    def _generate_fix_id(self, error_message: str, repository: str) -> str:
        """Generate unique ID for a fix"""
        content = f"{error_message}_{repository}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _get_fix_count(self) -> int:
        """Get total number of stored fixes"""
        try:
            collection = self.vectorstore.get()
            return len(collection.get('ids', []))
        except:
            return 0
    
    def clear_knowledge_base(self) -> bool:
        """Clear all stored fixes (use with caution)"""
        if not self.enabled:
            return False
        
        try:
            # Delete and recreate collection
            self.vectorstore.delete_collection()
            self._initialize_vectorstore()
            logger.warning("RAG knowledge base cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            return False


# Global RAG service instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get or create global RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
