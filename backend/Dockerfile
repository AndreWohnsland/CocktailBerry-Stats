FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12.10 /uv /uvx /bin/

WORKDIR /app

# build context is the repo root, the workspace lock there pins the
# backend dependencies so builds are reproducible
# --locked also fails the build if the lockfile is stale against the pyproject
COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/.python-version backend/
RUN uv sync --locked --no-dev --package backend

COPY backend/ backend/

WORKDIR /app/backend
EXPOSE 8000

# migrations run before the app serves, so the data always matches the deployed models
CMD ["sh", "-c", "uv run --no-sync python migrate.py && uv run --no-sync uvicorn app:app --host 0.0.0.0 --port 8000 --log-config=log_config.yaml"]
