from __future__ import annotations

import asyncio
import contextlib
import json
import time

import fastapi
import fastapi.testclient

import plugbear.fastapi


def test_register_async_handler() -> None:
    async def async_llm(context: plugbear.Request) -> str:
        await asyncio.sleep(0.1)
        return context.messages[0].content

    @contextlib.asynccontextmanager
    async def lifespan(app: fastapi.FastAPI):
        await plugbear.fastapi.register(
            app,
            llm_func=async_llm,
            api_key="some-api-key",
            endpoint="/plugbear",
        )
        yield

    app = fastapi.FastAPI(lifespan=lifespan)
    with fastapi.testclient.TestClient(app) as client:
        messages = dict(messages=[dict(content="some-chat", role="user1")])
        response = client.post("/plugbear", content=json.dumps(messages))
        assert response.status_code == 200
        assert response.text == messages["messages"][0]["content"]


def test_register_sync_handler() -> None:
    def async_llm(context: plugbear.Request) -> str:
        time.sleep(0.1)
        return context.messages[0].content

    @contextlib.asynccontextmanager
    async def lifespan(app: fastapi.FastAPI):
        await plugbear.fastapi.register(
            app,
            llm_func=async_llm,
            api_key="some-api-key",
            endpoint="/plugbear",
        )
        yield

    app = fastapi.FastAPI(lifespan=lifespan)
    with fastapi.testclient.TestClient(app) as client:
        messages = dict(messages=[dict(content="some-chat", role="user1")])
        response = client.post("/plugbear", content=json.dumps(messages))
        assert response.status_code == 200
        assert response.text == messages["messages"][0]["content"]
