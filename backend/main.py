from typing import Optional

from fastapi import Header
from models import CocktailData
from app import init_app


app, deta, isDev = init_app()
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
cocktail_deta = deta.Base(TABLE_NAME)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}


@app.post("/cocktail", tags=["cocktail"])
def insert_cocktaildata(cocktail: CocktailData, x_deta_api_key_name: Optional[str] = Header(None)):
    return cocktail_deta.insert({
        "cocktailname": cocktail.cocktailname[:30],  # limit by 30 chars
        "volume": cocktail.volume,
        "machinename": cocktail.machinename[:30],  # limit by 30 chars
        "countrycode": cocktail.countrycode,
        "keyname": x_deta_api_key_name,
        "makedate": cocktail.makedate,
    })
