import os
from deta import Deta
from fastapi import FastAPI
from dotenv import load_dotenv

from models import CocktailData

load_dotenv()
app = FastAPI()
isDev = os.getenv("DEBUG") is not None
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
cocktail_deta = deta.Base(TABLE_NAME)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}


@app.post("/cocktail")
def insert_cocktaildata(cocktail: CocktailData):
    return cocktail_deta.insert({
        "cocktailname": cocktail.cocktailname,
        "volume": cocktail.volume,
        "machinename": cocktail.machinename,
        "countrycode": cocktail.countrycode
    })
