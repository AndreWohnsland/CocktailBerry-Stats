"""Integration tests against a real (test) mongodb, covering migrations, routes, cleanup and cli."""

import datetime
from pathlib import Path

import environment
import httpx
import pytest
from app import app
from beanie.executors.migrate import MigrationSettings, run_migrate
from cli import app as cli_app
from conftest import MONGO_URI, TEST_DB
from models import ApiKeyDocument, CocktailDocument
from typer.testing import CliRunner
from utils import _run_cleanup

pytestmark = pytest.mark.mongo

_MIGRATIONS_PATH = Path(__file__).parent.parent / "backend" / "migrations"


async def _migrate(direction: str, distance: int = 0) -> None:
    settings = MigrationSettings(
        direction=direction,
        distance=distance,
        connection_uri=MONGO_URI,
        database_name=TEST_DB,
        path=_MIGRATIONS_PATH,
        use_transaction=False,
    )
    await run_migrate(settings)


async def test_migrations_forward_and_backward(mongo_db):
    legacy_base = {"volume": 200, "machinename": "M1", "countrycode": "en"}
    await mongo_db.cocktails.insert_many(
        [
            {
                **legacy_base,
                "cocktailname": "Normal",
                "keyname": "dev",
                "makedate": "05/09/2026, 21:30",
                "receivedate": "05/09/2026, 21:31",
            },
            {
                **legacy_base,
                "cocktailname": "GarbageDate",
                "keyname": "dev",
                "makedate": "not a date",
                "receivedate": "05/09/2026, 10:00",
            },
            {
                **legacy_base,
                "cocktailname": "DetaRelic",
                "keyname": None,
                "makedate": "01/01/2022, 12:00",
                "receivedate": "01/01/2022, 12:00",
            },
        ]
    )
    await mongo_db.installations.insert_one({"os": "Debian 12", "receivedate": "05/09/2026, 09:00"})

    await _migrate("FORWARD")

    normal = await mongo_db.cocktails.find_one({"cocktailname": "Normal"})
    assert normal["makedate"] == datetime.datetime(2026, 9, 5, 21, 30)
    assert normal["receivedate"] == datetime.datetime(2026, 9, 5, 21, 31)
    garbage = await mongo_db.cocktails.find_one({"cocktailname": "GarbageDate"})
    # unparseable makedate falls back to the receivedate of the document
    assert garbage["makedate"] == garbage["receivedate"] == datetime.datetime(2026, 9, 5, 10, 0)
    relic = await mongo_db.cocktails.find_one({"cocktailname": "DetaRelic"})
    assert relic["keyname"] == "deta-era"
    installation = await mongo_db.installations.find_one()
    assert installation["receivedate"] == datetime.datetime(2026, 9, 5, 9, 0)

    await _migrate("BACKWARD", distance=1)  # revert keyname fill
    await _migrate("BACKWARD", distance=1)  # revert datetime conversion

    normal = await mongo_db.cocktails.find_one({"cocktailname": "Normal"})
    assert normal["makedate"] == "05/09/2026, 21:30"
    relic = await mongo_db.cocktails.find_one({"cocktailname": "DetaRelic"})
    assert relic["keyname"] is None


@pytest.fixture
async def api_client(mongo_db):
    await ApiKeyDocument(name="tester", api_key="valid-test-key").save()
    await ApiKeyDocument(name="revoked", api_key="revoked-test-key", invalid=True).save()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


def _cocktail_payload(makedate: str) -> dict:
    return {
        "cocktailname": "Mojito",
        "volume": 200,
        "machinename": "M1",
        "countrycode": "de",
        "ingredients": [{"name": "rum", "volume": 40}],  # machines send this, the api must ignore it
        "makedate": makedate,
    }


@pytest.mark.parametrize("makedate", ["05/09/2026, 21:30", "2026-09-05T21:30:00"])
async def test_post_cocktail_accepts_both_date_formats(api_client, makedate):
    response = await api_client.post(
        "/api/v1/cocktail", json=_cocktail_payload(makedate), headers={"x-api-key": "valid-test-key"}
    )
    assert response.status_code == 200
    assert response.json()["makedate"] == "2026-09-05T21:30:00"
    stored = await CocktailDocument.find_one(CocktailDocument.cocktailname == "Mojito")
    assert stored is not None
    assert stored.keyname == "tester"


async def test_post_cocktail_rejects_garbage_date(api_client):
    response = await api_client.post(
        "/api/v1/cocktail", json=_cocktail_payload("garbage"), headers={"x-api-key": "valid-test-key"}
    )
    assert response.status_code == 422


@pytest.mark.parametrize("headers", [{}, {"x-api-key": "wrong"}, {"x-api-key": "revoked-test-key"}])
async def test_protected_route_rejects_bad_keys(api_client, headers):
    response = await api_client.post("/api/v1/cocktail", json=_cocktail_payload("2026-09-05T21:30:00"), headers=headers)
    assert response.status_code == 401


async def test_public_endpoints_return_data(api_client):
    await api_client.post(
        "/api/v1/cocktail", json=_cocktail_payload("2026-09-05T21:30:00"), headers={"x-api-key": "valid-test-key"}
    )
    cocktails = (await api_client.get("/api/v1/public/cocktails")).json()
    assert len(cocktails) == 1
    assert "keyname" not in cocktails[0]
    assert (await api_client.get("/api/v1/public/installations/count")).json() == 0


async def test_cleanup_removes_only_test_cocktails(mongo_db):
    now = datetime.datetime.now()
    base = {
        "volume": 100,
        "machinename": "M1",
        "countrycode": "en",
        "keyname": "dev",
        "makedate": now,
        "receivedate": now,
    }
    await mongo_db.cocktails.insert_many(
        [{**base, "cocktailname": "TestCocktail Deluxe"}, {**base, "cocktailname": "Mojito"}]
    )
    await _run_cleanup()
    remaining = await mongo_db.cocktails.distinct("cocktailname")
    assert remaining == ["Mojito"]


@pytest.fixture
def cli_settings(mongo_db_sync, monkeypatch):
    monkeypatch.setattr(environment.SETTINGS, "atlas_uri", MONGO_URI)
    monkeypatch.setattr(environment.Settings, "database_name", property(lambda self: TEST_DB))
    return mongo_db_sync


def test_cli_add_and_revoke_key(cli_settings):
    runner = CliRunner()
    result = runner.invoke(cli_app, ["add-key", "party-user"])
    assert result.exit_code == 0
    key = result.output.split(": ")[1].strip()
    assert len(key) == 32
    assert cli_settings.api_keys.find_one({"name": "party-user"})["api_key"] == key

    duplicate = runner.invoke(cli_app, ["add-key", "party-user"])
    assert duplicate.exit_code == 1

    revoke = runner.invoke(cli_app, ["revoke-key", "party-user"])
    assert revoke.exit_code == 0
    assert cli_settings.api_keys.find_one({"name": "party-user"})["invalid"] is True

    again = runner.invoke(cli_app, ["revoke-key", "party-user"])
    assert again.exit_code == 0
    assert "already revoked" in again.output


def test_cli_revoke_unknown_key_fails(cli_settings):
    result = CliRunner().invoke(cli_app, ["revoke-key", "ghost"])
    assert result.exit_code == 1
