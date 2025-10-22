import json
from typing import Optional, Any
from config import settings
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis = None
        self.enabled = settings.redis_available
        self._memory_cache = {}  # Fallback in-memory cache
    
    async def connect(self):
        if not self.enabled:
            logger.info("📦 Cache: Using in-memory fallback")
            return
        try:
            import redis.asyncio as aioredis
            self.redis = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("✅ Redis connected")
        except Exception as e:
            logger.warning(f"⚠️  Redis failed, using memory cache: {e}")
            self.enabled = False
    
    async def get(self, key: str) -> Optional[Any]:
        if self.redis and self.enabled:
            try:
                value = await self.redis.get(key)
                return json.loads(value) if value else None
            except Exception as e:
                logger.error(f"Redis GET error: {e}")
        return self._memory_cache.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = None):
        ttl = ttl or settings.CACHE_TTL
        if self.redis and self.enabled:
            try:
                await self.redis.setex(key, ttl, json.dumps(value))
                return
            except Exception as e:
                logger.error(f"Redis SET error: {e}")
        self._memory_cache[key] = value
    
    async def delete(self, key: str):
        if self.redis and self.enabled:
            try:
                await self.redis.delete(key)
            except Exception:
                pass
        self._memory_cache.pop(key, None)
    
    async def close(self):
        if self.redis:
            await self.redis.close()

cache = CacheService()
