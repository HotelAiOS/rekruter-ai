import logging

logger = logging.getLogger(__name__)

"""Seed company knowledge base with example data"""
from services.rag_service import get_rag
from config import settings
import sys

# Temporarily enable RAG for seeding
settings.USE_RAG_CONTEXT = True

def seed_knowledge():
    """Add example company knowledge"""
    rag = get_rag()
    
    if not rag:
        logger.info("❌ RAG not initialized")
        return
    
    # Example documents
    documents = [
        {
            "id": "culture_001",
            "text": "Our company values work-life balance and remote work flexibility. We have a flat hierarchy and encourage open communication. Team members are expected to be proactive and take ownership of their projects. We use Agile methodology with 2-week sprints.",
            "metadata": {
                "title": "Company Culture",
                "category": "culture",
                "company_id": "test_company"
            }
        },
        {
            "id": "tech_stack_001",
            "text": "Our tech stack includes Python (FastAPI, Django), PostgreSQL, Redis, Docker, Kubernetes. We deploy to AWS using Terraform. Frontend is React with TypeScript. We practice TDD and maintain 80%+ code coverage. CI/CD with GitHub Actions.",
            "metadata": {
                "title": "Technology Stack",
                "category": "tech",
                "company_id": "test_company"
            }
        },
        {
            "id": "ideal_candidate_001",
            "text": "Ideal candidates are self-starters who can work independently. They should have strong problem-solving skills and excellent communication. Previous experience with microservices architecture is a plus. We value learning mindset over years of experience.",
            "metadata": {
                "title": "Ideal Candidate Profile",
                "category": "hiring",
                "company_id": "test_company"
            }
        },
        {
            "id": "red_flags_001",
            "text": "Red flags include: frequent job hopping (3+ jobs in 2 years), lack of ownership in previous roles, poor code quality in take-home tests, inability to explain technical decisions, no interest in our product/mission.",
            "metadata": {
                "title": "Hiring Red Flags",
                "category": "hiring",
                "company_id": "test_company"
            }
        }
    ]
    
    # Add documents
    for doc in documents:
        rag.add_document(doc["id"], doc["text"], doc["metadata"])
    
    # Save to disk
    rag.save()
    
    logger.info(f"\n✅ Seeded {len(documents)} documents to knowledge base")
    
    # Test search
    logger.info("\n🔍 Testing RAG search...")
    results = rag.search("What do we look for in candidates?", top_k=2)
    for i, result in enumerate(results, 1):
        logger.info(f"\n{i}. {result['metadata']['title']}")
        logger.info(f"   Score: {result['score']:.2f}")
        logger.info(f"   Preview: {result['text'][:100]}...")

if __name__ == "__main__":
    seed_knowledge()
