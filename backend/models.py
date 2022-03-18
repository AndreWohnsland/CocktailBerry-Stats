from enum import Enum
from pydantic import BaseModel


class LandEnum(str, Enum):
    """Limits countrycodes to currently supported ones"""
    en = 'en'
    de = 'de'


class CocktailData(BaseModel):
    """Model for all needed cocktail data"""
    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
    makedate: str
