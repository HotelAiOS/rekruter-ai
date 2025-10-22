from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from config import settings
import httpx

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_basic():
    """Basic health check"""
    return {"status": "ok", "version": "1.0.0"}

@router.get("/detailed")
async def health_detailed(db: Session = Depends(get_db)):
    """Detailed health check with dependencies"""
    health = {
        "status": "ok",
        "version": "1.0.0",
        "checks": {}
    }
    
    # Database check
    try:
        db.execute(text("SELECT 1"))
        health["checks"]["database"] = "ok"
    except Exception as e:
        health["checks"]["database"] = f"error: {e}"
        health["status"] = "degraded"
    
    # Ollama check
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            health["checks"]["ollama"] = "ok" if response.status_code == 200 else "error"
    except Exception as e:
        health["checks"]["ollama"] = f"error: {e}"
        health["status"] = "degraded"
    
    # Feature flags
    health["checks"]["features"] = {
        "multi_agent": settings.USE_MULTI_AGENT,
        "rag": settings.USE_RAG_CONTEXT,
        "kaizen": settings.USE_KAIZEN_LEARNING
    }
    
    return health

@router.get("/ready")
async def readiness():
    """Kubernetes readiness probe"""
    return {"ready": True}

@router.get("/live")
async def liveness():
    """Kubernetes liveness probe"""
    return {"alive": True}
