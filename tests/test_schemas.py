"""The cocktail input schema must accept both machine date formats forever."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from schemas import CocktailData


def _cocktail(makedate: str) -> CocktailData:
    return CocktailData(cocktailname="Mojito", volume=200, machinename="M1", countrycode="de", makedate=makedate)


def test_legacy_string_format_is_accepted():
    # old field machines send this format, support must never break
    assert _cocktail("06/09/2026, 21:30").makedate == datetime(2026, 9, 6, 21, 30)


def test_naive_iso_is_accepted():
    assert _cocktail("2026-09-06T21:45:12").makedate == datetime(2026, 9, 6, 21, 45, 12)


def test_aware_iso_is_accepted():
    parsed = _cocktail("2026-09-06T21:45:00+02:00").makedate
    assert parsed.utcoffset() is not None
    assert parsed.astimezone(UTC).hour == 19


def test_garbage_date_is_rejected():
    with pytest.raises(ValidationError):
        _cocktail("yesterday-ish")


def test_unknown_countrycode_is_rejected():
    with pytest.raises(ValidationError):
        CocktailData(cocktailname="x", volume=1, machinename="m", countrycode="fr", makedate="2026-09-06T21:45:00")
