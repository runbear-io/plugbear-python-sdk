FROM python:3.11-slim as build
WORKDIR /opt/app
EXPOSE 8000
ENTRYPOINT ["poetry", "run", "python", "/opt/app/main.py"]

COPY poetry.lock pyproject.toml main.py ./
RUN pip install -U poetry \
    && poetry install --no-root --sync
