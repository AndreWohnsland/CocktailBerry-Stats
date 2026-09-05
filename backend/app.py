import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

from beanie import init_beanie
from core.metadata import DESCRIPTION, TAGS_METADATA, VERSION, Tags
from environment import SETTINGS
from fastapi import FastAPI
from models import ApiKeyDocument, CocktailDocument, InstallationDocument
from pymongo import AsyncMongoClient
from routes import public_router, router
from utils import run_cleanup_loop, setup_logging

_logger = logging.getLogger(__name__)


@asynccontextmanager
async def db_lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # Startup
    mongodb_client: AsyncMongoClient = AsyncMongoClient(SETTINGS.atlas_uri)
    database = mongodb_client.get_database(SETTINGS.database_name)
    await init_beanie(database, document_models=[CocktailDocument, InstallationDocument, ApiKeyDocument])
    ping_response = await database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        _logger.info("Connected to database cluster.")
    cleanup_task = asyncio.create_task(run_cleanup_loop())

    yield

    # Shutdown
    cleanup_task.cancel()
    with suppress(asyncio.CancelledError):
        await cleanup_task
    await mongodb_client.close()


setup_logging()

app = FastAPI(
    title="CocktailBerry Stats / Dashboard API",
    version=VERSION,
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
