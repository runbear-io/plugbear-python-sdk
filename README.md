# [PlugBear](https://plugbear.io/) Python SDK

Connect a custom LLM to PlugBear through a web server.

## FastAPI

### Installation

To install the PlugBear Python SDK, run the following command:

```bash
pip install 'plugbear[fastapi]'
```

### Usage

Here's a simple example to get you started:

```python
from fastapi import FastAPI

import plugbear
import plugbear.fastapi

app = FastAPI()
PLUGBEAR_API_KEY = ""
PLUGBEAR_ENDPOINT = "/plugbear"


@app.on_event("startup")
async def _startup():
    await plugbear.fastapi.register(
        app,
        llm_func=some_llm,
        api_key=PLUGBEAR_API_KEY,
        endpoint=PLUGBEAR_ENDPOINT,
    )


async def some_llm(context: plugbear.Request) -> str:
    # template prompt using `context` to your own LLM
    # and return result
    result: str = ...
    return result
```

## Other Web server frameworks

Although it does not yet provide an interface as convenient as FastAPI, it can be directly linked to PlugBear.

### Installation

To install the PlugBear Python SDK, run the following command:

```bash
pip install plugbear
```

### Usage

```python
from fastapi import FastAPI

import plugbear
import plugbear.fastapi

app = FastAPI()
PLUGBEAR_API_KEY = ""
PLUGBEAR_ENDPOINT = "/plugbear"


@app.on_event("startup")
async def _startup():
    await plugbear.fastapi.register(
        app,
        llm_func=some_llm,
        api_key=PLUGBEAR_API_KEY,
        endpoint=PLUGBEAR_ENDPOINT,
    )


async def some_llm(context: plugbear.Request) -> str:
    # template prompt using `context` to your own LLM
    # and return result
    result: str = ...
    return result
```
