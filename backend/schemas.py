from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator

# format old field machines send, they will keep doing so for years
LEGACY_DATEFORMAT = "%d/%m/%Y, %H:%M"


def _accept_legacy_format(value: object) -> object:
    if isinstance(value, str):
        try:
            return datetime.strptime(value, LEGACY_DATEFORMAT)
        except ValueError:
            return value
    return value


# datetime that also accepts the legacy string format besides ISO
LegacyDatetime = Annotated[datetime, BeforeValidator(_accept_legacy_format)]


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
    makedate: LegacyDatetime


class CocktailWithoutKey(BaseModel):
    """Model for all needed cocktail data without key."""

    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
    makedate: datetime | None
    receivedate: datetime


class InstallationData(BaseModel):
    """Model for all needed cocktail data."""

    os_version: str
