"""Seed the database with sample data for local development.

Uses the same env logic as the app, so with DEBUG set it fills the cocktailberry_dev database.
Run from the backend folder: uv run python seed_dev.py
"""

import asyncio
import datetime
import random

from beanie import init_beanie
from environment import SETTINGS
from models import ApiKeyDocument, CocktailDocument, InstallationDocument
from pymongo import AsyncMongoClient

DATEFORMAT_STR = "%d/%m/%Y, %H:%M"
DEV_API_KEY = "local-dev-key"
MACHINES = ["Berry One", "Cocktail Castle", "Party Pi"]
COCKTAILS = ["Mojito", "Mai Tai", "Cuba Libre", "Tequila Sunrise", "Long Island"]
OS_NAMES = ["Debian 12 (bookworm)", "Debian 11 (bullseye)", "Armbian 23.8", "Ubuntu 22.04"]


async def main() -> None:
    client: AsyncMongoClient = AsyncMongoClient(SETTINGS.atlas_uri)
    db_name = SETTINGS.database_name
    database = client.get_database(db_name)
    await init_beanie(database, document_models=[CocktailDocument, InstallationDocument, ApiKeyDocument])

    if await CocktailDocument.count() > 0:
        print(f"Database '{db_name}' already contains cocktail data, not seeding again.")
        await client.close()
        return

    rng = random.Random(42)
    now = datetime.datetime.now()
    cocktails = []
    for _ in range(150):
        made = now - datetime.timedelta(days=rng.randint(0, 60), minutes=rng.randint(0, 1440))
        cocktails.append(
            CocktailDocument(
                cocktailname=rng.choice(COCKTAILS),
                volume=rng.choice([125, 150, 200, 250, 300]),
                machinename=rng.choice(MACHINES),
                countrycode=rng.choice(["en", "de"]),
                keyname="dev",
                makedate=made.strftime(DATEFORMAT_STR),
                receivedate=made.strftime(DATEFORMAT_STR),
            )
        )
    await CocktailDocument.insert_many(cocktails)

    installations = [
        InstallationDocument(
            os=rng.choice(OS_NAMES),
            receivedate=(now - datetime.timedelta(days=rng.randint(0, 60))).strftime(DATEFORMAT_STR),
        )
        for _ in range(20)
    ]
    await InstallationDocument.insert_many(installations)

    await ApiKeyDocument(name="dev", api_key=DEV_API_KEY).save()
    print(f"Seeded '{db_name}': {len(cocktails)} cocktails, {len(installations)} installations.")
    print(f"API key for the protected routes (x-api-key header): {DEV_API_KEY}")
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
