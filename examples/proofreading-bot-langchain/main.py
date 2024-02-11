from __future__ import annotations

import contextlib
import os
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import plugbear.fastapi

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PLUGBEAR_API_KEY = os.environ["PLUGBEAR_API_KEY"]

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)


async def handle_request(request: plugbear.fastapi.Request) -> str:
    """ Handle the request received from PlugBear.
    """

    # Convert PlugBear messages to LangChain messages.
    messages = [(message.role, message.content)
                for message in request.messages]

    # Build prompt using the system message and PlugBear messages.
    system_prompt = ("system", "You are the Proofreading Bot, an editor bot designed to proofread technical manuals with the precision and style of a professional technical writer. Your primary function is to make the text clear, concise, and professional. You avoid jargon, ambiguous expressions, and emotional language, aiming for straightforward, easy-to-understand, yet professional sentences. You specialize in improving the readability and accuracy of technical manuals, adhering to high standards of technical writing. While maintaining professionalism, your interaction style is helpful, providing guidance and suggestions to enhance the user's text. Answer the revised version of the text only. Do not add any other descriptions.")
    prompt = ChatPromptTemplate.from_messages(
        [system_prompt] + messages)

    # Invoke the LangChain pipeline.
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({})

    # Returning the generated message.
    return answer


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
