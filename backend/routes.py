import datetime

from fastapi import APIRouter, Request, Security
from models import ApiKeyDocument, CocktailDocument, InstallationDocument
from rate_limiting import limiter
from schemas import CocktailData, CocktailWithoutKey, InstallationData
from security import get_api_key

DATEFORMAT_STR = "%d/%m/%Y, %H:%M"

router = APIRouter(prefix="/api/v1", tags=["protected"])
public_router = APIRouter(prefix="/api/v1/public", tags=["public"])


@router.get("/", tags=["protected"])
async def check_api(api_key: ApiKeyDocument = Security(get_api_key)):
    """Route to check if api is working."""
    return {"message": f"Welcome to the API of the CocktailBerry-WebApp, user: {api_key.name}"}


@router.post("/cocktail", tags=["cocktail"])
async def insert_cocktaildata(cocktail: CocktailData, api_key: ApiKeyDocument = Security(get_api_key)):
    """Insert the cocktail data into the database.

    Route is protected by API key.
    """
    return await CocktailDocument(
        cocktailname=cocktail.cocktailname[:30],  # limit by 30 chars
        volume=cocktail.volume,
        machinename=cocktail.machinename[:30],  # limit by 30 chars
        countrycode=cocktail.countrycode,
        keyname=api_key.name,
        makedate=cocktail.makedate,
        receivedate=datetime.datetime.now().strftime(DATEFORMAT_STR),
    ).create()


@public_router.get("/cocktails", tags=["cocktail"], response_model=list[CocktailWithoutKey])
async def get_cocktaildata() -> list[CocktailWithoutKey]:
    """Get the cocktail data from the database.

    Route is open accessible.
    """
    return await CocktailDocument.find_all().project(CocktailWithoutKey).to_list()


@public_router.post("/installation", tags=["installation"])
@limiter.limit("1/minute")
async def post_installation(request: Request, information: InstallationData):
    """Endpoint to post information about successful installation.

    Route is open accessible.
    """
    return await InstallationDocument(
        os=information.os_version, receivedate=datetime.datetime.now().strftime(DATEFORMAT_STR)
    ).create()


@public_router.get("/installations", tags=["installation"], response_model=list[InstallationDocument])
async def get_installations() -> list[InstallationDocument]:
    """Endpoint to receive information about successful installation.

    Route is open accessible.
    """
    return await InstallationDocument.find_all().to_list()


@public_router.get("/installations/count", tags=["installation"])
async def get_installation_count():
    """Endpoint to receive information about successful installation count.

    Route is open accessible.
    """
    installation_data = await InstallationDocument.find_all().to_list()
    return len(installation_data)
