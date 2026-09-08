from datetime import datetime
from typing import ClassVar

from beanie import Document
from pymongo import ASCENDING, IndexModel
from schemas import LandEnum


class CocktailDocument(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: LandEnum
    keyname: str
    # wall clock time on the machine, no timezone by design (hour of day analytics)
    makedate: datetime
    # utc instant when the api received the data
    receivedate: datetime

    class Settings:  # noqa: D106
        name = "cocktails"


class InstallationDocument(Document):
    os: str
    receivedate: datetime

    class Settings:  # noqa: D106
        name = "installations"


class ApiKeyDocument(Document):
    name: str
    api_key: str
    invalid: bool | None = False

    class Settings:  # noqa: D106
        name = "api_keys"
        # looked up on every protected request, unique also guards against ambiguous keys
        indexes: ClassVar[list[IndexModel]] = [IndexModel([("api_key", ASCENDING)], unique=True)]
