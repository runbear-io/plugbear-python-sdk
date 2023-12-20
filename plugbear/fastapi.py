from __future__ import annotations

import inspect
from collections.abc import Coroutine, Sequence
from typing import Any, Optional, Protocol, Union, cast, runtime_checkable

import fastapi
import fastapi.responses
import pydantic.dataclasses

import plugbear

__all__ = ("Message", "Request", "LLMHandler", "register")


@pydantic.dataclasses.dataclass(frozen=True)
class Message:
    role: str
    content: str
    name: Optional[str] = None


@pydantic.dataclasses.dataclass(frozen=True)
class Request:
    messages: Sequence[Message]


@runtime_checkable
class LLMHandler(Protocol):
    def __call__(self, request: Request) -> Union[str, Coroutine[Any, Any, str]]:
        pass


async def register(app: fastapi.FastAPI, *, llm_func: LLMHandler, api_key: str, endpoint: str) -> None:
    await plugbear.PlugBear.init(api_key=api_key)

    if inspect.iscoroutinefunction(llm_func):

        @app.post(endpoint, response_class=fastapi.responses.PlainTextResponse)
        async def plugbear_callback(request: Request) -> str:
            return cast(str, await llm_func(request))
    else:

        @app.post(endpoint, response_class=fastapi.responses.PlainTextResponse)
        def plugbear_callback(request: Request) -> str:
            return cast(str, llm_func(request))
