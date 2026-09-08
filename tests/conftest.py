import os

import pandas as pd
import pytest

# must happen before any backend module import, environment.py requires it
os.environ.setdefault("ATLAS_URI", "mongodb://localhost:27017")

from beanie import init_beanie
from models import ApiKeyDocument, CocktailDocument, InstallationDocument
from pymongo import AsyncMongoClient, MongoClient

from frontend.models import CocktailSchema, InstallationSchema

MONGO_URI = os.environ["ATLAS_URI"]
# never derived from SETTINGS, so no env mistake can point tests at dev or prod data
TEST_DB = "cocktailberry_test"
_SKIP_MSG = "no mongodb reachable, start it with: docker compose up -d mongo (backend folder)"
_COLLECTIONS = ("cocktails", "installations", "api_keys", "migrations_log")

_mongo_available: bool | None = None


def _ensure_mongo_available() -> None:
    global _mongo_available  # noqa: PLW0603
    if _mongo_available is None:
        client: MongoClient = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1500)
        try:
            client.admin.command("ping")
            _mongo_available = True
        except Exception:
            _mongo_available = False
        finally:
            client.close()
    if not _mongo_available:
        pytest.skip(_SKIP_MSG)


@pytest.fixture
async def mongo_db():
    """Yield a clean test database with beanie initialized on it."""
    _ensure_mongo_available()
    client: AsyncMongoClient = AsyncMongoClient(MONGO_URI)
    db = client.get_database(TEST_DB)
    for collection in _COLLECTIONS:
        await db.drop_collection(collection)
    await init_beanie(db, document_models=[CocktailDocument, InstallationDocument, ApiKeyDocument])
    yield db
    await client.close()


@pytest.fixture
def mongo_db_sync():
    """Sync variant for tests that cannot run in an event loop (typer CliRunner)."""
    _ensure_mongo_available()
    client: MongoClient = MongoClient(MONGO_URI)
    db = client.get_database(TEST_DB)
    for collection in _COLLECTIONS:
        db.drop_collection(collection)
    yield db
    client.close()


@pytest.fixture
def cocktails_df() -> pd.DataFrame:
    """Six cocktails across three machines, two languages and known dates."""
    base = pd.Timestamp(2026, 8, 1, 18, 0)
    return pd.DataFrame(
        {
            CocktailSchema.language: ["en", "de", "en", "de", "en", "en"],
            CocktailSchema.machine_name: ["M1", "M2", "M1", "M2", "M3", "M1"],
            CocktailSchema.cocktail_name: ["Mojito", "Mai Tai", "Mojito", "Mojito", "Cuba Libre", "Mai Tai"],
            CocktailSchema.volume: [230, 260, 240, 210, 300, 260],
            CocktailSchema.receivedate: [base + pd.Timedelta(days=i * 3, hours=i) for i in range(6)],
        }
    )


@pytest.fixture
def installations_df() -> pd.DataFrame:
    base = pd.Timestamp(2026, 8, 1, 18, 0)
    return pd.DataFrame(
        {
            InstallationSchema.OS: ["Debian 12", "Debian 11", "Armbian 23", "Ubuntu"],
            InstallationSchema.RECEIVEDATE: [base + pd.Timedelta(days=i * 9) for i in range(4)],
        }
    )
