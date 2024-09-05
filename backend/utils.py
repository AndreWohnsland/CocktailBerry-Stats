import re

from fastapi.logger import logger
from fastapi_utilities import repeat_every
from models import CocktailDocument


@repeat_every(seconds=60 * 20)  # 20 minutes
async def run_cleanup() -> None:
    """Route which is triggered on deta action."""
    logger.warning("Running cleanup")
    to_delete: list[CocktailDocument] = await CocktailDocument.find(
        {"cocktailname": re.compile("testcocktail", re.IGNORECASE)}
    ).to_list()
    if len(to_delete) > 0:
        logger.warning("Deleting %s number of items named testcocktail", len(to_delete))
    for cocktail in to_delete:
        logger.warning("Deleting item: %s", cocktail)
        await cocktail.delete()
