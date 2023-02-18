from enum import Enum
from typing import Optional
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


class DetaCocktail(BaseModel):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: Optional[str]
    makedate: Optional[str]
    receivedate: str
