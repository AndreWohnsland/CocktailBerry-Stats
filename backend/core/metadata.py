from enum import StrEnum

VERSION = "1.4.1"

DESCRIPTION = """
An endpoint for [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) to send cocktail data to! 🍹

## cocktail

You can **post your cocktaildata** or **get all the cocktaildata**.
Check the tags which route is public accessible and which one is protected by an API key.
Usually routes inserting or changing data are protected, routes getting data are open.

This API is still quite minimal, since not much endpoints are needed for CocktailBerry.
"""


class Tags(StrEnum):
    COCKTAIL = "cocktail"
    INSTALLATION = "installation"
    PROTECTED = "protected"
    PUBLIC = "public"


TAGS_METADATA = [
    {
        "name": Tags.COCKTAIL,
        "description": "Operations with cocktail data.",
    },
    {
        "name": Tags.INSTALLATION,
        "description": "Topics related to CocktailBerry installation.",
    },
    {
        "name": Tags.PROTECTED,
        "description": "Route is protected by API key.",
    },
    {
        "name": Tags.PUBLIC,
        "description": "Route is accessible by public.",
    },
]
