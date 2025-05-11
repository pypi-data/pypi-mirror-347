import asyncio
from abc import ABC, abstractmethod
from typing import Any


class CacheABC(ABC):
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    @abstractmethod
    async def get(self, key: str, default: Any = None) -> Any:
        return default

    @abstractmethod
    async def set(self, key: str, value: Any, timeout_seconds: int = None) -> bool:
        return True

    @abstractmethod
    def delete(self, key: str) -> bool:
        return True

    async def get_or_set(self, key: str, value: Any = None) -> Any:
        result = await self.get(key)
        if result is not None:
            return result

        await self.set(key, value)
        return value

    async def exists(self, key: str) -> bool:
        return await self.get(key) is not None
