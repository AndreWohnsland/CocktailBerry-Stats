import os
from deta import Deta
from fastapi import FastAPI
from dotenv import load_dotenv


__DESC = """
An endpoint for [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) to send cocktail data to! 🍹

## cocktail

You can **post your cocktaildata**.

This API is still quite minimal, since not much endpoints are needed for CocktailBerry.
"""


def init_app():
    load_dotenv()
    tags_metadata = [
        {
            "name": "cocktail",
            "description": "Operations with cocktail data.",
        },
    ]
    app = FastAPI(
        title="CocktailBerry WebApp / Dashboard API",
        version="1.0",
        description=__DESC,
        openapi_tags=tags_metadata,
    )
    is_dev = os.getenv("DEBUG") is not None
    deta = Deta(os.getenv("DETA_PROJECT_KEY"))
    return app, deta, is_dev
