"""Plugbear easily integrates LLM into various channels."""

from __future__ import annotations

import dataclasses
import http
from collections.abc import Sequence

import aiohttp

__version__ = "0.1.0"
__all__ = ("Message", "Request", "PlugBear", "PlugBearError", "UnauthorizedOrganization")


@dataclasses.dataclass(frozen=True)
class Message:
    role: str
    chat: str


@dataclasses.dataclass(frozen=True)
class Request:
    messages: Sequence[Message]


@dataclasses.dataclass(frozen=True)
class PlugBear:
    api_key: str

    @classmethod
    async def init(cls, api_key: str) -> PlugBear:
        pb = PlugBear(api_key=api_key)
        await pb.verify()
        return pb

    async def verify(self) -> None:
        try:
            headers = {"X-SDK-Version": __version__, "Authorization": self.api_key}
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get("https://plugbear.io/api/sdk/verify") as res:
                    if res.status != http.HTTPStatus.OK:
                        raise UnauthorizedOrganization(await res.text())
        except aiohttp.ClientError as err:
            raise PlugBearError("Unknown error") from err


class PlugBearError(Exception):
    pass


class UnauthorizedOrganization(PlugBearError):
    pass
