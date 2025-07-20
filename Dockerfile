FROM ghcr.io/astral-sh/uv:alpine AS builder

ADD . /app
WORKDIR /app
RUN uv sync --locked --compile-bytecode

CMD ["uv", "run", "main.py"]
