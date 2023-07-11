import datetime
from typing import Optional

from fastapi import Header
from fastapi.logger import logger
from models import CocktailData, DetaCocktail, DetaEvent, InstallationData
from app import init_app


app, deta, isDev = init_app()
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
cocktail_deta = deta.Base(TABLE_NAME)
_INSTALLATION_TBL = "installation" + ("_dev" if isDev else "")
installation_deta = deta.Base(_INSTALLATION_TBL)
DATEFORMAT_STR = "%d/%m/%Y, %H:%M"


@app.get("/", tags=["protected"])
def check_api():
    """Route to check if api is working"""
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}


@app.post("/cocktail", tags=["cocktail", "protected"])
def insert_cocktaildata(cocktail: CocktailData, x_deta_api_key_name: Optional[str] = Header(None)):
    """Insert the cocktail data into the database.
    Route is protected by API key.
    """
    return cocktail_deta.insert(
        {
            "cocktailname": cocktail.cocktailname[:30],  # limit by 30 chars
            "volume": cocktail.volume,
            "machinename": cocktail.machinename[:30],  # limit by 30 chars
            "countrycode": cocktail.countrycode,
            "keyname": x_deta_api_key_name,
            "makedate": cocktail.makedate,
            "receivedate": datetime.datetime.now().strftime(DATEFORMAT_STR),
        }
    )


@app.get("/public/cocktails", tags=["cocktail", "open"], response_model=list[DetaCocktail])
def get_cocktaildata() -> list[DetaCocktail]:
    """Get the cocktail data from the database.
    Route is open accessible."""
    res = cocktail_deta.fetch(limit=10000)
    cocktails: list[DetaCocktail] = res.items
    while res.last:
        res = cocktail_deta.fetch(limit=10000, last=res.last)
        cocktails += res.items
    return cocktails


@app.post("/public/installation", tags=["installation", "open"])
def post_installation(information: InstallationData):
    """Endpoint to post information about successful installation.
    Route is open accessible."""
    return installation_deta.insert(
        {
            "receivedate": datetime.datetime.now().strftime(DATEFORMAT_STR),
            "os": information.os_version,
        }
    )


@app.get("/public/installations", tags=["installation", "open"])
def get_installations():
    """Endpoint to receive information about successful installation.
    Route is open accessible."""
    res = installation_deta.fetch(limit=10000)
    installations: list = res.items
    while res.last:
        res = installation_deta.fetch(limit=10000, last=res.last)
        installations += res.items
    return len(installations)


@app.post("/__space/v0/actions", tags=["automation", "protected"])
def run_actions(event_object: DetaEvent) -> None:
    """Route which is triggered on deta action.
    The event data with id / trigger is provided in the event object.
    """
    event = event_object.event
    if event.id == "cleanup":
        to_delete: list[dict] = cocktail_deta.fetch({"cocktailname?contains": "testcocktail"}).items
        if len(to_delete) > 0:
            logger.warning("Deleting %s number of items named testcocktail", len(to_delete))
        for cocktail in to_delete:
            logger.warning("Deleting item: %s", cocktail)
            cocktail_deta.delete(key=cocktail["key"])
