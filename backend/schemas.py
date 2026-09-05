from enum import StrEnum

from pydantic import BaseModel


class LandEnum(StrEnum):
    """Limits country codes to currently supported ones."""

    en = "en"
    de = "de"


class CocktailData(BaseModel):
    """Model for all needed cocktail data."""

    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
    makedate: str


class CocktailWithoutKey(BaseModel):
    """Model for all needed cocktail data without key."""

    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
    makedate: str
    receivedate: str


class InstallationData(BaseModel):
    """Model for all needed cocktail data."""

    os_version: str
