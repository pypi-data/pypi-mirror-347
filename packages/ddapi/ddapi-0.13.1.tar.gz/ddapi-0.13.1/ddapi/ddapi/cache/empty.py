from typing import Any

from ddapi.cache import CacheABC


class EmptyCache(CacheABC):
    async def get(self, key: str, default: Any = None) -> Any:
        return default

    async def set(self, key: str, value: Any, timeout_seconds: int = None) -> bool:
        return True

    def delete(self, key: str) -> bool:
        return True
