# Some Dev Notes

## Manage API Keys

API keys live in the `api_keys` collection and are checked by the backend on the protected routes.
A key document has a `name`, the `api_key` value and an `invalid` flag.
Create a new key by inserting a document, for example from the `backend` folder:

```python
import asyncio
import secrets

from beanie import init_beanie
from environment import SETTINGS
from models import ApiKeyDocument
from pymongo import AsyncMongoClient


async def main() -> None:
    client: AsyncMongoClient = AsyncMongoClient(SETTINGS.atlas_uri)
    await init_beanie(client.get_database(SETTINGS.database_name), document_models=[ApiKeyDocument])
    key = secrets.token_urlsafe(32)
    await ApiKeyDocument(name="some-user", api_key=key).save()
    print(f"Created key for some-user: {key}")
    await client.close()


asyncio.run(main())
```

Run it with `uv run python <script>.py`, the env decides if the dev or the main database is used.

## Revoke API Keys

Set the `invalid` flag of the key document to `true`.
The backend rejects revoked keys on the protected routes.
Prefer revoking over deleting, so the key name stays around for the existing cocktail data.

## Version Bumps

The release tag, the root `pyproject.toml` and `backend/pyproject.toml` must carry the same version.
The API reads its version from `backend/pyproject.toml` at startup.
The release workflow verifies all of this and blocks the release on a mismatch.
