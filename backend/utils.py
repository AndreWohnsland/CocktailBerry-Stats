import asyncio
import logging
import re

from models import CocktailDocument

_logger = logging.getLogger(__name__)
_CLEANUP_INTERVAL_SECONDS = 60 * 20


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-9s [%(name)s] %(message)s")


async def run_cleanup_loop() -> None:
    """Run the test data cleanup immediately and then every interval, until cancelled."""
    while True:
        try:
            await _run_cleanup()
        except Exception:
            # keep the loop alive, a transient db error must not stop future cleanups
            _logger.exception("Cleanup run failed")
        await asyncio.sleep(_CLEANUP_INTERVAL_SECONDS)


async def _run_cleanup() -> None:
    """Delete test data (cocktails named testcocktail) from the database."""
    _logger.warning("Running cleanup")
    to_delete: list[CocktailDocument] = await CocktailDocument.find(
        {"cocktailname": re.compile("testcocktail", re.IGNORECASE)}
    ).to_list()
    if len(to_delete) > 0:
        _logger.warning("Deleting %s number of items named testcocktail", len(to_delete))
    for cocktail in to_delete:
        _logger.warning("Deleting item: %s", cocktail)
        await cocktail.delete()
