# Some Dev Notes

## Generate new API keys

If you have owner acces to deta, you can run:

```bash
deta auth create-api-key --name "keyname" --desc "Desc for key"
deta auth delete-api-key --name "keyname"
```

to manage the API key creation. Also get further help from `deta help` or the [official docs](https://docs.deta.sh/docs/micros/api_keys).

## The .deta Folder

[The Docs](https://docs.deta.sh/docs/micros/faqs_micros/#is-it-safe-to-commit-the-deta-folder-created-by-the-cli) state it is safe to commit the .deta folder. I will still not commit it, since it got instance related data and in case of a new person cloning the repository this would make no sense that it points to my instance. The new user will probably want to generate his own.

## Migration

Script used for the migration, data extracted from deta.

```python
import json
from pathlib import Path

from beanie import init_beanie
from environment import CONNECTION_STRING
from fastapi.logger import logger
from models import ApiKeyDocument, CocktailDocument, InstallationDocument
from motor.motor_asyncio import AsyncIOMotorClient

bases = Path(__file__).resolve().parent / "bases"
installations = bases / "installation.json"
cocktails = bases / "cocktails.json"


async def init_db():
    # Startup
    mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    database = mongodb_client.get_database("cocktailberry")
    await init_beanie(database, document_models=[CocktailDocument, InstallationDocument, ApiKeyDocument])
    ping_response = await database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    logger.info("Connected to database cluster.")


async def run_main():
    await init_db()
    # read in installations.json and convert into python
    with installations.open("r", encoding="utf-8") as f:
        installations_data = json.loads(f.read())
    # read in cocktails.json
    with cocktails.open("r", encoding="utf-8") as f:
        cocktails_data = json.loads(f.read())
    print(len(installations_data))
    for installation in installations_data:
        await InstallationDocument(
            os=installation["os"],
            receivedate=installation["receivedate"]
        ).create()
    print(len(cocktails_data))
    for cocktail in cocktails_data:
        await CocktailDocument(
            cocktailname=cocktail["cocktailname"],
            volume=cocktail["volume"],
            machinename=cocktail["machinename"],
            countrycode=cocktail["countrycode"],
            keyname=cocktail["keyname"],
            makedate=cocktail["makedate"],
            receivedate=cocktail["receivedate"]
        ).create()
    print("done")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_main())
```