import aioredis
import json
from typing import Optional, Any
from config import settings
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis = None
        self.enabled = settings.redis_available
    
    async def connect(self):
        if not self.enabled:
            return
        try:
            self.redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("✅ Redis connected")
        except Exception as e:
            logger.warning(f"⚠️  Redis connection failed: {e}")
            self.enabled = False
    
    async def get(self, key: str) -> Optional[Any]:
        if not self.enabled or not self.redis:
            return None
        try:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None):
        if not self.enabled or not self.redis:
            return
        try:
            ttl = ttl or settings.CACHE_TTL
            await self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
    
    async def delete(self, key: str):
        if not self.enabled or not self.redis:
            return
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
    
    async def close(self):
        if self.redis:
            await self.redis.close()

cache = CacheService()
