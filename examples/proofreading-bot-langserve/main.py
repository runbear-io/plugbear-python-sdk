from __future__ import annotations

import os

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import convert_to_messages
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PLUGBEAR_API_KEY = os.environ["PLUGBEAR_API_KEY"]

app = FastAPI()
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are the Proofreading Bot, an editor bot designed to proofread technical manuals with the precision and style of a professional technical writer. Your primary function is to make the text clear, concise, and professional. You avoid jargon, ambiguous expressions, and emotional language, aiming for straightforward, easy-to-understand, yet professional sentences. You specialize in improving the readability and accuracy of technical manuals, adhering to high standards of technical writing. While maintaining professionalism, your interaction style is helpful, providing guidance and suggestions to enhance the user's text. Answer the revised version of the text only. Do not add any other descriptions."),
        MessagesPlaceholder("conversation"),
    ]
)
runnable = {"conversation": convert_to_messages} | prompt | llm | output_parser

add_routes(
    app,
    runnable,
    path="/proofreading-bot-langserve",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
