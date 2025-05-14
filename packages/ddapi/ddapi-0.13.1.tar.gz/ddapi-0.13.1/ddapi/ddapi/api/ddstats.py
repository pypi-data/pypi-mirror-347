from urllib.parse import quote

from .._api import API
from ..scheme import (
    DProfile,
    SMap,
    Maps,
    Player,
)

__all__ = ("DDstats",)


class DDstats(API):
    @property
    def domain(self) -> str:
        return "ddstats.tw"

    @staticmethod
    def powered() -> str:
        return DDstats().domain

    async def profile(self, player_name: str) -> DProfile:
        return await self._generate_model_instance(
            f"https://{self.domain}/profile/json?player={quote(player_name)}",
            DProfile,
            "profile",
        )

    async def map(self, map_name: str) -> SMap:
        return await self._generate_model_instance(
            f"https://{self.domain}/map/json?map={quote(map_name)}", SMap
        )

    async def maps(self) -> Maps:
        return await self._generate_model_instance(
            f"https://{self.domain}/maps/json", Maps, "maps"
        )

    async def player(self, player_name: str) -> Player:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(
            f"https://{self.domain}/player/json?player={quote(player_name)}", Player
        )
