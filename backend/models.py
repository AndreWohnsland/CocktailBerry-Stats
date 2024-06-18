from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LandEnum(str, Enum):
    """Limits country codes to currently supported ones."""

    en = 'en'
    de = 'de'


class CocktailData(BaseModel):
    """Model for all needed cocktail data."""

    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
    makedate: str


class InstallationData(BaseModel):
    """Model for all needed cocktail data."""

    os_version: str


class DetaCocktail(BaseModel):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: Optional[str]
    makedate: Optional[str]
    receivedate: str


class DetaInstallation(BaseModel):
    os: str
    receivedate: str


class DetaEventData(BaseModel):
    id: str
    trigger: str


class DetaEvent(BaseModel):
    event: DetaEventData
