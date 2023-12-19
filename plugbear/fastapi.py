from __future__ import annotations

import inspect
from collections.abc import Coroutine
from typing import Any, Protocol, Union, runtime_checkable

import fastapi

import plugbear

__all__ = ("LLMHandler", "register")


@runtime_checkable
class LLMHandler(Protocol):
    def __call__(self, request: plugbear.Request) -> Union[str, Coroutine[Any, Any, str]]:
        pass


async def register(app: fastapi.FastAPI, *, llm_func: LLMHandler, api_key: str, endpoint: str) -> None:
    await plugbear.PlugBear.init(api_key=api_key)

    if inspect.iscoroutinefunction(llm_func):

        @app.post(endpoint)
        async def plugbear_callback(request: plugbear.Request) -> str:
            return await llm_func(request)
    else:

        @app.post(endpoint)
        def plugbear_callback(request: plugbear.Request) -> str:
            return llm_func(request)
