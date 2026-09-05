from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from models import ApiKeyDocument

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> ApiKeyDocument:
    """Validate the API key from the x-api-key HTTP header.

    Raises an HTTPException if the key is missing, unknown or revoked (invalid flag).
    """
    api_key = await ApiKeyDocument.find(ApiKeyDocument.api_key == api_key_header).first_or_none()
    if api_key is not None and not api_key.invalid:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
