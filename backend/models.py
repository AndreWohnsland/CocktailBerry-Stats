from datetime import datetime

from beanie import Document


class CocktailDocument(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: str | None
    # wall clock time on the machine, no timezone by design (hour of day analytics)
    makedate: datetime | None
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
