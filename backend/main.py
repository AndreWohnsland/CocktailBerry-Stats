import os
from deta import Deta
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
isDev = os.getenv("DEBUG") is not None
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
cocktails = deta.Base(TABLE_NAME)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}
