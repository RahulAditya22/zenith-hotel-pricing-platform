import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

from app.core.config import settings

logger = logging.getLogger("zenith.cache")


class BaseCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass


class InMemoryCache(BaseCache):
    """
    Thread-safe, async in-memory cache with TTL support.
    Used as fallback when Redis is not configured or unavailable.
    """

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key not in self._store:
                return None
            val, expires_at = self._store[key]
            if time.time() > expires_at:
                del self._store[key]
                return None
            return json.loads(val) if isinstance(val, str) else val

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        async with self._lock:
            expires_at = time.time() + ttl
            serialized = (
                json.dumps(value)
                if not isinstance(value, (int, float, str, bool, type(None)))
                else value
            )
            self._store[key] = (serialized, expires_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._store.clear()


class RedisCache(BaseCache):
    """
    Redis implementation using redis.asyncio client.
    """

    def __init__(self, redis_url: str) -> None:
        import redis.asyncio as aioredis

        self._client = aioredis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        try:
            val = await self._client.get(key)
            if val is None:
                return None
            try:
                return json.loads(val)
            except json.JSONDecodeError:
                return val
        except Exception as e:
            logger.warning(f"Redis get failed: {e}. Falling back to cache miss.")
            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        try:
            serialized = (
                json.dumps(value)
                if not isinstance(value, (int, float, str, bool, type(None)))
                else value
            )
            await self._client.set(key, serialized, ex=ttl)
        except Exception as e:
            logger.warning(f"Redis set failed: {e}")

    async def delete(self, key: str) -> None:
        try:
            await self._client.delete(key)
        except Exception as e:
            logger.warning(f"Redis delete failed: {e}")

    async def clear(self) -> None:
        try:
            await self._client.flushdb()
        except Exception as e:
            logger.warning(f"Redis clear failed: {e}")


# Singleton cache instance
_cache_instance: Optional[BaseCache] = None


def get_cache() -> BaseCache:
    global _cache_instance
    if _cache_instance is None:
        if settings.REDIS_URL:
            try:
                _cache_instance = RedisCache(settings.REDIS_URL)
                logger.info("Initialized Redis cache layer.")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis ({e}), using InMemoryCache fallback.")
                _cache_instance = InMemoryCache()
        else:
            logger.info("No REDIS_URL provided. Initialized clean InMemoryCache layer.")
            _cache_instance = InMemoryCache()
    return _cache_instance
