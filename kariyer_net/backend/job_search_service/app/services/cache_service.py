import json
from typing import Optional, Any
from ..core.cache import get_cache

class CacheService:
    def __init__(self):
        self.cache = get_cache()

    async def get_cached_jobs(self, cache_key: str) -> Optional[Any]:
        """Get cached job search results"""
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        return None

    async def cache_jobs(self, cache_key: str, jobs_data: Any, expire_time: int = 3600):
        """Cache job search results"""
        self.cache.setex(cache_key, expire_time, json.dumps(jobs_data))

    async def invalidate_cache(self, pattern: str):
        """Invalidate cache by pattern"""
        keys = self.cache.keys(pattern)
        if keys:
            self.cache.delete(*keys) 