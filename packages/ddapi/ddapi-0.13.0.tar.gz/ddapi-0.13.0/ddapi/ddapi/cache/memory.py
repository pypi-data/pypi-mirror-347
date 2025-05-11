import asyncio
from typing import Any

from .base import CacheABC


class MemoryCache(CacheABC):
    async def get(self, key: str, default: Any = None) -> Any:
        async with self._lock:
            return self._cache.get(key, default)

    async def set(self, key: str, value: Any, timeout_seconds: int = None) -> bool:
        async with self._lock:
            if timeout_seconds is None:
                self._cache[key] = value
                return True
            asyncio.create_task(self._remove_after_timeout(key, timeout_seconds))
            return True

    async def delete(self, key: str) -> bool:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def _remove_after_timeout(self, key: str, timeout: int):
        await asyncio.sleep(timeout)
        await self.delete(key)
