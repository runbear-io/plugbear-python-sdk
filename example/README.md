# PlugBear Python SDK Example (FastAPI)

## Prerequisites

- Docker

## Usage

```shell
docker build . -t plugbear-python-sdk-example
docker run --rm -ti \
  -p 8000:8000 \
  -e PLUGBEAR_API_KEY="YOUR.PLUGBEAR.API.KEY" \
  -e OPENAI_API_KEY="YOUR.OPENAI.API.KEY" \
  plugbear-python-sdk-example
```

You can also existing assistant by passing `OPENAI_ASSISTANT_ID` environment to `docker run`.
