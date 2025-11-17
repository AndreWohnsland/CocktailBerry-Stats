FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .python-version ./ 
RUN uv sync

COPY . /app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-config=log_config.yaml"] 