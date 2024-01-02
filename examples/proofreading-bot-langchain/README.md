# PlugBear Python SDK Example (LangChain)

This project introduces an example of integrating a LangChain application with
communication channels, such as Slack, using PlugBear. Check [Building a Proofreading Bot Using LangChain](http://localhost:3001/use-cases/proofreading-bot/langchain) for detailed guide.

## Prerequisites

- [Poetry](https://python-poetry.org)

## Development

### Installing Dependencies

Use [Poetry](https://python-poetry.org/) to install dependencies.

```bash
poetry install
```

### Running Server

Run the command below to run the server:

```bash
OPENAI_API_KEY="YOUR_OPENAI_API_KEY" \
  PLUGBEAR_API_KEY="YOUR_PLUGBEAR_API_KEY" \
  poetry run python main.py
```

You can obtain your `OPENAI_API_KEY` from the
[OpenAI API Keys](https://platform.openai.com/api-keys) page, and your
`PLUGBEAR_API_KEY` from the
[PlugBear API Keys](https://auth.plugbear.io/org/api_keys) page.

### Testing Integration

Follow [PlugBear Documentation](https://docs.plugbear.io) to connect your app
into communication channels and test it.

Ask any math question to `@PlugBear` after connecting it. e.g.,
``@PlugBear This is an example sentence.``.
