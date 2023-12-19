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
import contextlib

import plugbear
import plugbear.fastapi
from fastapi import FastAPI

PLUGBEAR_API_KEY = ""
PLUGBEAR_ENDPOINT = "/plugbear"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await plugbear.fastapi.register(
        app,
        llm_func=some_llm,
        api_key=PLUGBEAR_API_KEY,
        endpoint=PLUGBEAR_ENDPOINT,
    )
    yield


app = FastAPI(lifespan=lifespan)


async def some_llm(context: plugbear.Request) -> str:
    # template prompt using `context` to your own LLM
    # and return result
    result: str = ...
    return result
```


<details>
  <summary>For versions below 0.93.0</summary>

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

</details>

## Other Web server frameworks

Although it does not yet provide an interface as convenient as FastAPI, it can be directly linked to PlugBear.

### Installation

```bash
pip install plugbear
```

### Usage

Taking Django as an example, it looks like this:

#### settings.py

```python
import plugbear
from asgiref.sync import async_to_sync

PLUGBEAR_API_KEY = ""
PLUGBEAR_ENDPOINT = "/plugbear"

pb = async_to_sync(plugbear.PlugBear.init(api_key=PLUGBEAR_API_KEY))
```

#### urls.py

```python
from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path(settings.PLUGBEAR_ENDPOINT, views.handle_plugbear, name="plugbear"),
]
```
#### views.py

```python
import plugbear
from dacite import from_dict
from django.http import HttpResponse


def handle_plugbear(request):
    context = from_dict(data_class=plugbear.Request, data=request.data)
    result = some_llm(context)
    return HttpResponse(result)

def some_llm(context: plugbear.Request) -> str:
    # template prompt using `context` to your own LLM
    # and return result
    result: str = ...
    return result
```
