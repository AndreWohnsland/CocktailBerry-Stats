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
    result = await CocktailDocument.find({"cocktailname": re.compile("testcocktail", re.IGNORECASE)}).delete()
    if result is not None and result.deleted_count > 0:
        _logger.warning("Cleanup removed %s testcocktail entries", result.deleted_count)
