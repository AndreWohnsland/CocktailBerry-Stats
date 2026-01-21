import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from beanie import init_beanie
from core.metadata import DESCRIPTION, TAGS_METADATA, VERSION, Tags
from environment import CONNECTION_STRING, is_dev
from fastapi import FastAPI
from models import ApiKeyDocument, CocktailDocument, InstallationDocument
from pymongo import AsyncMongoClient
from routes import public_router, router
from utils import run_cleanup, setup_logging

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def db_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    mongodb_client: AsyncMongoClient = AsyncMongoClient(CONNECTION_STRING)
    database = mongodb_client.get_database("cocktailberry" + ("_dev" if is_dev else ""))
    await init_beanie(database, document_models=[CocktailDocument, InstallationDocument, ApiKeyDocument])
    ping_response = await database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        _logger.info("Connected to database cluster.")
    await run_cleanup()

    yield

    # Shutdown
    await mongodb_client.close()


setup_logging()

app = FastAPI(
    title="CocktailBerry WebApp / Dashboard API",
    version="1.1",
    description=DESCRIPTION,
    openapi_tags=TAGS_METADATA,
    lifespan=db_lifespan,
)
app.include_router(router)
app.include_router(public_router)


@app.get("/version", tags=[Tags.PUBLIC])
async def get_version() -> dict:
    """Get the current version of the API."""
    return {"version": VERSION}
