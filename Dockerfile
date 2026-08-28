FROM python:3.10-slim-trixie

LABEL owner="Braeson Nyahera" \
	  version="1.0.0" \
	  description="Binance Crypto prices extraction ETL"

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy \
	PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-dev --no-install-project

COPY main.py ./
COPY app ./app

RUN uv sync --frozen --no-dev

ENTRYPOINT ["price-tracker"]