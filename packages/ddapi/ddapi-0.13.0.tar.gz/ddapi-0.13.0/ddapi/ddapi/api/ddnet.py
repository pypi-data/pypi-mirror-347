from urllib.parse import quote

from .._api import API
from ..scheme import (
    DDPlayer,
    DDStatus,
    ReleasesMaps,
    Query,
    QueryMap,
    QueryMapper,
    Master,
    DMap,
)

__all__ = ("DDnetApi",)

from ..enum import MasterEnum


class DDnetApi(API):
    @property
    def domain(self) -> str:
        return "ddnet.org"

    @staticmethod
    def powered() -> str:
        return DDnetApi().domain

    async def player(self, player: str) -> DDPlayer:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(
            f"https://{self.domain}/players/?json2={quote(player)}", DDPlayer
        )

    async def status(self) -> DDStatus:
        return await self._generate_model_instance(
            f"https://{self.domain}/status/json/stats.json", DDStatus
        )

    async def releases_map(self) -> ReleasesMaps:
        return await self._generate_model_instance(
            f"https://{self.domain}/releases/maps.json", ReleasesMaps, "maps"
        )

    async def query(self, player: str) -> Query:
        return await self._generate_model_instance(
            f"https://{self.domain}/players/?query={quote(player)}", Query, "players"
        )

    async def query_map(self, map_name: str) -> QueryMap:
        return await self._generate_model_instance(
            f"https://{self.domain}/maps/?query={quote(map_name)}",
            QueryMap,
            "maps",
        )

    async def query_mapper(self, player: str) -> QueryMapper:
        return await self._generate_model_instance(
            f"https://{self.domain}/maps/?qmapper={quote(player)}",
            QueryMapper,
            "players",
        )

    async def master(self, number: MasterEnum = MasterEnum.master1) -> Master:
        return await self._generate_model_instance(
            f"https://master{number}.{self.domain}/ddnet/15/servers.json", Master
        )

    async def map(self, map_name: str) -> DMap:
        return await self._generate_model_instance(
            f"https://{self.domain}/maps/?json={quote(map_name)}", DMap
        )
