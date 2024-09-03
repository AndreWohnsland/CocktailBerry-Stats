from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from models import ApiKeyDocument

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> ApiKeyDocument:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
    ----
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
    -------
        The validated API key.

    Raises:
    ------
        HTTPException: If the API key is invalid or missing.

    """
    api_key = await ApiKeyDocument.find(ApiKeyDocument.api_key == api_key_header).first_or_none()
    if api_key is not None:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
