import logging
import re

from fastapi_utilities import repeat_every
from models import CocktailDocument

_logger = logging.getLogger(__name__)


@repeat_every(seconds=60 * 20)  # 20 minutes
async def run_cleanup() -> None:
    """Route which is triggered on deta action."""
    _logger.warning("Running cleanup")
    to_delete: list[CocktailDocument] = await CocktailDocument.find(
        {"cocktailname": re.compile("testcocktail", re.IGNORECASE)}
    ).to_list()
    if len(to_delete) > 0:
        _logger.warning("Deleting %s number of items named testcocktail", len(to_delete))
    for cocktail in to_delete:
        _logger.warning("Deleting item: %s", cocktail)
        await cocktail.delete()
