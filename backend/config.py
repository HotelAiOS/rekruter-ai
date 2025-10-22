from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./rekruter.db"
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_TIMEOUT: int = 120
    ANTHROPIC_API_KEY: Optional[str] = None
    SECRET_KEY: str = "dev-secret-key"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_VERSION: str = "1.0.0"
    SENTRY_DSN: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    CACHE_TTL: int = 3600
    USE_MULTI_AGENT: bool = True
    USE_RAG_CONTEXT: bool = True
    USE_KAIZEN_LEARNING: bool = True
    ENABLE_FALLBACK: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MAX_UPLOAD_SIZE: int = 10485760
    PAGINATION_PAGE_SIZE: int = 20
    
    model_config = ConfigDict(env_file=".env", case_sensitive=False)
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.DATABASE_URL.lower()
    
    @property
    def redis_available(self) -> bool:
        return self.REDIS_ENABLED and bool(self.REDIS_URL)

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
