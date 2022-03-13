from models import CocktailData
from app import init_app


app, deta, isDev = init_app()
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
cocktail_deta = deta.Base(TABLE_NAME)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}


@app.post("/cocktail", tags=["cocktail"])
def insert_cocktaildata(cocktail: CocktailData):
    return cocktail_deta.insert({
        "cocktailname": cocktail.cocktailname,
        "volume": cocktail.volume,
        "machinename": cocktail.machinename,
        "countrycode": cocktail.countrycode
    })
