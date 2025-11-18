from __future__ import annotations

import httpx

from backend.common.config import get_settings
from backend.udm_ausf.schemas.auth import UEAuthRequest, UEAuthResponse

settings = get_settings()


async def authenticate_with_udm(payload: UEAuthRequest) -> UEAuthResponse:
    async with httpx.AsyncClient(base_url=settings.udm_ausf_base_url, timeout=5.0) as client:
        response = await client.post("/auth/ue-auth", json=payload.model_dump())
        response.raise_for_status()
        return UEAuthResponse.model_validate(response.json())
