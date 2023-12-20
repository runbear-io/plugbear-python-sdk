# PlugBear Python SDK Example (FastAPI)

## Prerequisites

- Docker

## Usage

This will create a math tutor AI.
You can make a query on any integrated channel, like this: ``@PlugBear "I need to solve the equation `3x + 11 = 14`. Can you help me?"``.

```shell
docker build . -t plugbear-python-sdk-example
docker run --rm -ti \
  -p 8000:8000 \
  -e PLUGBEAR_API_KEY="YOUR.PLUGBEAR.API.KEY" \
  -e OPENAI_API_KEY="YOUR.OPENAI.API.KEY" \
  plugbear-python-sdk-example
```

You can also existing assistant by passing `OPENAI_ASSISTANT_ID` environment to `docker run`.
