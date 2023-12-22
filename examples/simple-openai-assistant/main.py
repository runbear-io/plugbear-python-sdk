from __future__ import annotations

import asyncio
import contextlib
import os
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from openai import AsyncOpenAI

import plugbear.fastapi


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PLUGBEAR_API_KEY = os.environ["PLUGBEAR_API_KEY"]
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def handle_request(request: plugbear.fastapi.Request) -> str:
    """ Handle the request received from PlugBear.
    """
    # Finding or creating an example OpenAI Assistant.
    assistant_id = await find_or_create_example_assistant()

    # Creating a new OpenAI thread for the request.
    thread = await openai_client.beta.threads.create()

    # Adding messages to the thread. Adjust the message for your use case.
    for message in request.messages:
        await openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message.content,
        )

    # Generating a response from the OpenAI Assistant.
    run = await openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Polling until the response is ready.
    while run.status != "completed":
        await asyncio.sleep(1)
        run = await openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Returning the generated message.
    resp = await openai_client.beta.threads.messages.list(thread_id=thread.id, order="desc")
    generated_messages = [
        content.text.value for content in resp.data[0].content]
    return "\n".join(generated_messages)


async def find_or_create_example_assistant() -> str:
    """ Find or create an example of an OpenAI Assistant named 'Math Tutor'.
    """
    assistants = await openai_client.beta.assistants.list()
    tutors = [a for a in assistants.data if a.name == "Math Tutor"]
    if len(tutors) > 0:
        assistant = tutors[0]
    else:
        assistant = await openai_client.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview",
        )

    return assistant.id


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await plugbear.fastapi.register(
        app,
        llm_func=handle_request,
        api_key=PLUGBEAR_API_KEY,
        endpoint="/plugbear",
    )

    yield


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
