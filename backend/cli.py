"""CLI tools for the backend.

Run from the backend folder, the env decides if the dev or the main database is used:
uv run python cli.py add-key "keyname"
"""

import asyncio
import secrets

import typer
from beanie import init_beanie
from environment import SETTINGS
from models import ApiKeyDocument
from pymongo import AsyncMongoClient

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback() -> None:
    """CLI tools for the CocktailBerry-Stats backend."""


@app.command()
def add_key(name: str) -> None:
    """Create an api key for the given name, insert it into the db and print it."""
    api_key = asyncio.run(_insert_key(name))
    typer.echo(f"API key for '{name}': {api_key}")


@app.command()
def revoke_key(name: str) -> None:
    """Revoke the api key with the given name, the protected routes reject it afterwards."""
    asyncio.run(_revoke_key(name))


async def _insert_key(name: str) -> str:
    client = await _connect()
    if await ApiKeyDocument.find(ApiKeyDocument.name == name).first_or_none() is not None:
        typer.echo(f"A key named '{name}' already exists, pick another name or revoke the old one first.", err=True)
        raise typer.Exit(1)
    api_key = secrets.token_urlsafe(24)  # 24 bytes -> exactly 32 url-safe chars
    await ApiKeyDocument(name=name, api_key=api_key).save()
    await client.close()
    return api_key


async def _revoke_key(name: str) -> None:
    client = await _connect()
    key_doc = await ApiKeyDocument.find(ApiKeyDocument.name == name).first_or_none()
    if key_doc is None:
        typer.echo(f"No key named '{name}' found.", err=True)
        raise typer.Exit(1)
    if key_doc.invalid:
        typer.echo(f"Key '{name}' is already revoked.")
    else:
        key_doc.invalid = True
        await key_doc.save()
        typer.echo(f"Revoked key '{name}'.")
    await client.close()


async def _connect() -> AsyncMongoClient:
    client: AsyncMongoClient = AsyncMongoClient(SETTINGS.atlas_uri)
    await init_beanie(client.get_database(SETTINGS.database_name), document_models=[ApiKeyDocument])
    return client


if __name__ == "__main__":
    app()
