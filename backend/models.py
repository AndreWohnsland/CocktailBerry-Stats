from enum import Enum
from typing import Optional

from beanie import Document


class LandEnum(str, Enum):
    """Limits country codes to currently supported ones."""

    en = 'en'
    de = 'de'


class CocktailDocument(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: Optional[str]
    makedate: Optional[str]
    receivedate: str

    class Settings:  # noqa: D106
        name = "cocktails"


class InstallationDocument(Document):
    os: str
    receivedate: str

    class Settings:  # noqa: D106
        name = "installations"
