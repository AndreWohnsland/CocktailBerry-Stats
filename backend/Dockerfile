FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12.10 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .python-version ./ 
RUN uv sync

COPY . /app

EXPOSE 8000

# migrations run before the app serves, so the data always matches the deployed models
CMD ["sh", "-c", "uv run python migrate.py && uv run uvicorn app:app --host 0.0.0.0 --port 8000 --log-config=log_config.yaml"] 