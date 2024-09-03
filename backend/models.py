from typing import Optional

from beanie import Document


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


class ApiKeyDocument(Document):
    name: str
    api_key: str
    invalid: Optional[bool] = False

    class Settings:  # noqa: D106
        name = "api_keys"
