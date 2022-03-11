import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
isDev = os.getenv("DEBUG") is not None


@app.get("/")
def read_root():
    return {"message": "Welcome to the API of the CocktailBerry-WebApp"}
