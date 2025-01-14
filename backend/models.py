from beanie import Document


class CocktailDocument(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: str | None
    makedate: str | None
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
    invalid: bool | None = False

    class Settings:  # noqa: D106
        name = "api_keys"
