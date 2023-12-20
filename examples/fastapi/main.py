from __future__ import annotations

import asyncio
import contextlib
import os
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from openai import AsyncOpenAI
from openai.pagination import AsyncCursorPage
from openai.types.beta.threads import MessageContentText, ThreadMessage

import plugbear.fastapi


# create a OpenAI Assistant if the user does not enter an OpenAi Assistant ID.
async def _get_openai_assistant_id(client: AsyncOpenAI) -> str:
    try:
        return os.environ["OPENAI_ASSISTANT_ID"]
    except KeyError:
        assistant = await client.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview",
        )
        return assistant.id


openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
openai_assistant_id = asyncio.get_event_loop().run_until_complete(_get_openai_assistant_id(openai_client))


async def openai_assistant(request: plugbear.fastapi.Request) -> str:
    thread = await openai_client.beta.threads.create()

    joined_msg = "\n".join(m.content for m in request.messages)
    await openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=joined_msg,
    )

    run = await openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=openai_assistant_id,
        instructions="Please address the user as Jane Doe. The user has a premium account.",
    )

    while run.status != "completed":
        await asyncio.sleep(1)
        run = await openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = await openai_client.beta.threads.messages.list(thread_id=thread.id)
    print(messages)
    return _join_assistant_messages(messages)


def _join_assistant_messages(m: AsyncCursorPage[ThreadMessage]) -> str:
    messages: list[str] = []
    for data in m.data:
        if data.role != "assistant":
            continue

        for content in data.content:
            if not isinstance(content, MessageContentText):
                continue
            messages.append(content.text.value)

    return "\n".join(messages)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await plugbear.fastapi.register(
        app,
        llm_func=openai_assistant,
        api_key=os.environ["PLUGBEAR_API_KEY"],
        endpoint=os.getenv("PLUGBEAR_ENDPOINT", default="/plugbear"),
    )

    yield


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
