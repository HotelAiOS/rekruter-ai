from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from config import settings
from database import engine
from middleware.security import limiter, request_id_middleware, security_headers_middleware
from services.cache import cache
import logging

logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0 if settings.is_development else 0.1,
    )
    logger.info("🔍 Sentry monitoring enabled")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Rekruter AI starting (env: {settings.ENVIRONMENT})...")
    await cache.connect()
    yield
    logger.info("🛑 Shutting down...")
    await cache.close()
    await engine.dispose()

app = FastAPI(
    title="Rekruter AI",
    version=settings.API_VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(request_id_middleware)
app.middleware("http")(security_headers_middleware)

if settings.is_production or settings.DEBUG:
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    logger.info("📊 Prometheus metrics at /metrics")

@app.get("/health")
async def health_check():
    from database import check_db_connection
    db_status = await check_db_connection()
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status.get("status", "unknown"),
        "features": {
            "multi_agent": settings.USE_MULTI_AGENT,
            "rag": settings.USE_RAG_CONTEXT,
            "kaizen": settings.USE_KAIZEN_LEARNING,
            "cache": cache.enabled,
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc) if settings.DEBUG else None}
    )

from routers import jobs, candidates, auth
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {
        "message": "Rekruter AI API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }
