from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status

from backend.common.config import get_settings


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    settings = get_settings()
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


def api_key_dependency(_: None = Depends(verify_api_key)) -> None:
    return None
