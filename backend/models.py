from enum import Enum
from pydantic import BaseModel


class LandEnum(str, Enum):
    en = 'en'
    de = 'de'


class CocktailData(BaseModel):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
