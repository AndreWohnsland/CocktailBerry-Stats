"""Migrate the legacy string dates ("%d/%m/%Y, %H:%M") to real datetime fields.

makedate stays machine wall clock time, receivedate is a utc instant.
An unparseable makedate falls back to the receivedate of the document.
An unparseable receivedate aborts the migration, it is server generated and must be valid.
"""

import logging
from datetime import datetime

from beanie import Document, iterative_migration

LEGACY_DATEFORMAT = "%d/%m/%Y, %H:%M"
_logger = logging.getLogger(__name__)


# the old models must declare every field, undeclared fields would be dropped on replace
class OldCocktail(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: str | None
    makedate: str | None
    receivedate: str

    class Settings:  # noqa: D106
        name = "cocktails"


class NewCocktail(Document):
    cocktailname: str
    volume: int
    machinename: str
    countrycode: str
    keyname: str | None
    makedate: datetime | None
    receivedate: datetime

    class Settings:  # noqa: D106
        name = "cocktails"


class OldInstallation(Document):
    os: str
    receivedate: str

    class Settings:  # noqa: D106
        name = "installations"


class NewInstallation(Document):
    os: str
    receivedate: datetime

    class Settings:  # noqa: D106
        name = "installations"


class Forward:
    @iterative_migration()
    async def cocktail_dates_to_datetime(self, input_document: OldCocktail, output_document: NewCocktail) -> None:
        receivedate = datetime.strptime(input_document.receivedate, LEGACY_DATEFORMAT)
        output_document.receivedate = receivedate
        makedate = None
        if input_document.makedate is not None:
            try:
                makedate = datetime.strptime(input_document.makedate, LEGACY_DATEFORMAT)
            except ValueError:
                _logger.warning(
                    "Unparseable makedate %r on cocktail %s, falling back to receivedate",
                    input_document.makedate,
                    input_document.id,
                )
                makedate = receivedate
        output_document.makedate = makedate

    @iterative_migration()
    async def installation_dates_to_datetime(
        self, input_document: OldInstallation, output_document: NewInstallation
    ) -> None:
        output_document.receivedate = datetime.strptime(input_document.receivedate, LEGACY_DATEFORMAT)


class Backward:
    @iterative_migration()
    async def cocktail_dates_to_string(self, input_document: NewCocktail, output_document: OldCocktail) -> None:
        output_document.receivedate = input_document.receivedate.strftime(LEGACY_DATEFORMAT)
        output_document.makedate = (
            input_document.makedate.strftime(LEGACY_DATEFORMAT) if input_document.makedate is not None else None
        )

    @iterative_migration()
    async def installation_dates_to_string(
        self, input_document: NewInstallation, output_document: OldInstallation
    ) -> None:
        output_document.receivedate = input_document.receivedate.strftime(LEGACY_DATEFORMAT)
