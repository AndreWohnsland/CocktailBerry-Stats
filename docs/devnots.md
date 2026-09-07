# Some Dev Notes

## Manage API Keys

API keys live in the `api_keys` collection and are checked by the backend on the protected routes.
A key document has a `name`, the `api_key` value and an `invalid` flag.
Create a new key with the backend cli from the `backend` folder:

```bash
uv run python cli.py add-key "some-user"
```

It generates a random key, inserts it and prints it once.
The env decides if the dev or the main database is used.

## Revoke API Keys

```bash
uv run python cli.py revoke-key "some-user"
```

This sets the `invalid` flag of the key document, the backend rejects revoked keys on the protected routes.
Prefer revoking over deleting, so the key name stays around for the existing cocktail data.

## Database Migrations

Schema migrations live in `backend/migrations` and use the beanie migration framework.
The container runs `migrate.py` before the app starts, applied migrations are tracked in the `migrations_log` collection.
Add a new migration as a timestamped file with `Forward` and `Backward` classes, see the existing one as reference.
Roll the newest migration back with `uv run python migrate.py backward` and redeploy the previous image.
Take a `mongodump` before deploying a migration that rewrites existing data.

## Version Bumps

The release tag, the root `pyproject.toml` and `backend/pyproject.toml` must carry the same version.
The API reads its version from `backend/pyproject.toml` at startup.
The release workflow verifies all of this and blocks the release on a mismatch.
