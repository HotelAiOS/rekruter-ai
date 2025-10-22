import logging

logger = logging.getLogger(__name__)

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from typing import List, Dict, Optional
from config import settings
import pickle
from pathlib import Path

class CompanyKnowledgeRAG:
    """RAG system for company-specific knowledge"""
    
    def __init__(self):
        logger.info("🔧 Initializing RAG system...")
        # Load embedding model
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Model dimension
        
        # Initialize FAISS index
        self.index_path = Path("data/company_knowledge.index")
        self.docs_path = Path("data/company_docs.pkl")
        
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.docs_path, 'rb') as f:
                self.documents = pickle.load(f)
            logger.info(f"✅ Loaded {len(self.documents)} documents from cache")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []
            logger.info("✅ Created new RAG index")
    
    def add_document(self, doc_id: str, text: str, metadata: Dict):
        """Add document to knowledge base"""
        # Create embedding
        embedding = self.encoder.encode(text)
        
        # Add to FAISS
        self.index.add(np.array([embedding]))
        
        # Store document
        self.documents.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata,
            "embedding": embedding
        })
        
        logger.info(f"✅ Added document: {doc_id}")
    
    def search(self, query: str, top_k: int = 3, company_id: Optional[str] = None) -> List[Dict]:
        """Search for relevant documents"""
        if self.index.ntotal == 0:
            return []
        
        # Encode query
        query_embedding = self.encoder.encode(query)
        
        # Search
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        
        # Get results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]
                
                # Filter by company_id if provided
                if company_id and doc["metadata"].get("company_id") != company_id:
                    continue
                
                results.append({
                    "text": doc["text"],
                    "metadata": doc["metadata"],
                    "score": float(distance)
                })
        
        return results
    
    def build_context(self, query: str, company_id: Optional[str] = None) -> str:
        """Build context string for AI from knowledge base"""
        results = self.search(query, company_id=company_id, top_k=3)
        
        if not results:
            return "No relevant company context found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            title = result["metadata"].get("title", "Untitled")
            text = result["text"][:500]  # Limit length
            context_parts.append(f"[Document {i}: {title}]\n{text}")
        
        return "\n\n".join(context_parts)
    
    def save(self):
        """Save index and documents to disk"""
        self.index_path.parent.mkdir(exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        
        with open(self.docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
        
        logger.info(f"✅ Saved {len(self.documents)} documents to {self.index_path}")

# Global instance (lazy load when RAG is enabled)
_rag_instance = None

def get_rag():
    """Get or create RAG instance"""
    global _rag_instance
    if _rag_instance is None and settings.USE_RAG_CONTEXT:
        _rag_instance = CompanyKnowledgeRAG()
    return _rag_instance
