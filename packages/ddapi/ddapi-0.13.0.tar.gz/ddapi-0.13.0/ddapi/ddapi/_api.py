import asyncio
import logging
from abc import ABC
from typing import Optional, Type, Any

import aiohttp
from aiohttp import ClientSession

from ddapi.cache import CacheABC, EmptyCache
from ddapi.types import T

try:
    import orjson

    DEFAULT_JSON_DECODER = orjson.loads
except ImportError:
    from aiohttp.typedefs import DEFAULT_JSON_DECODER

logger = logging.getLogger(__name__)

class API(ABC):
    def __init__(
        self,
        session: ClientSession = None,
        *,
        autoclose: bool = True,
        cache: CacheABC = EmptyCache(),
        json_loads: Any = DEFAULT_JSON_DECODER,
    ):
        self.__session = session
        self.cache = cache
        self.json_loads = json_loads
        self.autoclose = autoclose

        if self.__session is None:
            self.__session = aiohttp.ClientSession()
            logger.debug("Created a new aiohttp ClientSession.")

    async def __aenter__(self):
        if self.__session is None:
            self.__session = aiohttp.ClientSession()
            logger.debug("Created a new aiohttp ClientSession on enter.")
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        if self.autoclose:
            logger.debug("Closing aiohttp ClientSession on exit.")
            await self.close()

    def __del__(self):
        if self.__session is not None and not self.__session.closed:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                logger.warning("Closing aiohttp ClientSession in the background.")
                loop.create_task(self.close())
            else:
                logger.warning("Closing aiohttp ClientSession synchronously.")
                loop.run_until_complete(self.close())

    async def _get(self, url: str) -> Optional[dict]:
        """Send a GET request to the given URL and return the response as JSON."""
        logger.debug(f"Sending GET request to {url}.")
        async with self.__session.get(url) as req:
            if req.status == 200:
                logger.debug(f"Received response from {url}: {req.status}.")
                return await req.json(loads=self.json_loads)
            logger.error(f"Failed to get response from {url}: {req.status}.")
            return None

    async def _generate_model_instance(
        self,
        url: str,
        model: Type[T],
        k: Optional[str] = None,
        cache_timeout: int = 300,
    ) -> Optional[T]:
        """Generate a model instance from the given URL and optional keyword arguments.

        Args:
            url (str): The URL to fetch data from.
            model (Type[ModelType]): The model class to instantiate.
            k (str, optional): An optional keyword to wrap the data in a dictionary.

        Returns:
            Optional[ModelType]: A model instance.
        """
        cache = await self.cache.get(url)
        if cache is not None:
            return cache

        dat = await self._get(url)
        if dat is None or not dat:
            logger.warning(f"No data received from {url}.")
            return None

        data = model(**{k: dat} if k is not None else dat)
        await self.cache.set(url, data, cache_timeout)
        return data

    async def is_closed(self) -> bool:
        """True is closed, False otherwise."""
        return self.__session is None or self.__session.closed

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.__session is not None:
            logger.debug("Closing aiohttp ClientSession.")
            await self.__session.close()
        self.__session = None
        self.cache = None

    @property
    def domain(self) -> str:
        return ""

    @staticmethod
    def powered() -> None:
        return None
