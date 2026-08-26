FROM python:3.10-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml, uv.lock, .python-version  app/

RUN uv sync --frozen 