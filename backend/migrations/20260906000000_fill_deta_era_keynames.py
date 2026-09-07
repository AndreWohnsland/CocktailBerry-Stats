"""Replace the null keynames from the deta era with an explicit marker.

The api sets keyname from the api key on every insert since the deta migration,
so today a null keyname is impossible, only old data carries it.
"""

from datetime import datetime

from beanie import Document, iterative_migration

DETA_ERA_KEYNAME = "deta-era"


# default None also covers documents where the field is missing entirely
class OldCocktail(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: str | None = None
    makedate: datetime
    receivedate: datetime

    class Settings:  # noqa: D106
        name = "cocktails"


class NewCocktail(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: str
    makedate: datetime
    receivedate: datetime

    class Settings:  # noqa: D106
        name = "cocktails"


class Forward:
    @iterative_migration()
    async def fill_null_keynames(self, input_document: OldCocktail, output_document: NewCocktail) -> None:
        output_document.keyname = input_document.keyname or DETA_ERA_KEYNAME


class Backward:
    @iterative_migration()
    async def restore_null_keynames(self, input_document: NewCocktail, output_document: OldCocktail) -> None:
        output_document.keyname = None if input_document.keyname == DETA_ERA_KEYNAME else input_document.keyname
