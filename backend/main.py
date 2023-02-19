import datetime
from typing import Optional

from fastapi import Header
from models import CocktailData, DetaCocktail
from app import init_app


app, deta, isDev = init_app()
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
cocktail_deta = deta.Base(TABLE_NAME)


@app.get("/", tags=["protected"])
def check_api():
    """Route to check if api is working"""
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}


@app.post("/cocktail", tags=["cocktail", "protected"])
def insert_cocktaildata(cocktail: CocktailData, x_deta_api_key_name: Optional[str] = Header(None)):
    """Insert the cocktail data into the database.
    Route is protected by API key.
    """
    return cocktail_deta.insert({
        "cocktailname": cocktail.cocktailname[:30],  # limit by 30 chars
        "volume": cocktail.volume,
        "machinename": cocktail.machinename[:30],  # limit by 30 chars
        "countrycode": cocktail.countrycode,
        "keyname": x_deta_api_key_name,
        "makedate": cocktail.makedate,
        "receivedate": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M"),
    })


@app.get("/public/cocktails", tags=["cocktail", "open"], response_model=list[DetaCocktail])
def get_cocktaildata() -> list[DetaCocktail]:
    """Get the cocktail data from the database.
    Route is open accessible."""
    cocktails: list[DetaCocktail] = cocktail_deta.fetch().items
    return cocktails
