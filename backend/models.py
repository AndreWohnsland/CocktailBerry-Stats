from pydantic import BaseModel


class CocktailData(BaseModel):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
