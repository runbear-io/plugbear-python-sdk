from __future__ import annotations

import inspect
from collections.abc import Coroutine, Sequence
from typing import Any, Optional, Protocol, Union, runtime_checkable

import fastapi
from pydantic import BaseModel

import plugbear

__all__ = ("Message", "Request", "LLMHandler", "register")


class Message(BaseModel):
    role: str
    content: str
    name: Optional[str] = None

    class Config:
        frozen = True


class Request(BaseModel):
    messages: Sequence[Message]

    class Config:
        frozen = True


@runtime_checkable
class LLMHandler(Protocol):
    def __call__(self, request: Request) -> Union[str, Coroutine[Any, Any, str]]:
        pass


async def register(app: fastapi.FastAPI, *, llm_func: LLMHandler, api_key: str, endpoint: str) -> None:
    await plugbear.PlugBear.init(api_key=api_key)

    if inspect.iscoroutinefunction(llm_func):

        @app.post(endpoint, response_class=fastapi.responses.PlainTextResponse)
        async def plugbear_callback(request: Request) -> str:
            return await llm_func(request)
    else:

        @app.post(endpoint, response_class=fastapi.responses.PlainTextResponse)
        def plugbear_callback(request: Request) -> str:
            return llm_func(request)
