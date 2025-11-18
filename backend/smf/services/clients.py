from __future__ import annotations

import httpx

from backend.common.config import get_settings
from backend.nssf.schemas.slice import SliceSelectionRequest, SliceSelectionResponse
from backend.pcf.schemas.policy import PolicyRead
from backend.upf.schemas.session import UPFSessionCreate, UPFSessionRead

settings = get_settings()


async def request_slice_selection(requested_slice: str | None) -> SliceSelectionResponse:
    payload = SliceSelectionRequest(
        requested_sst=requested_slice,
        ue_profile=requested_slice,
    )
    async with httpx.AsyncClient(base_url=settings.nssf_base_url, timeout=5.0) as client:
        response = await client.post("/nssf/select-slice", json=payload.model_dump())
        response.raise_for_status()
        return SliceSelectionResponse.model_validate(response.json())


async def fetch_policy_for_slice(slice_id: str) -> PolicyRead | None:
    async with httpx.AsyncClient(base_url=settings.pcf_base_url, timeout=5.0) as client:
        response = await client.get(f"/pcf/policies/slice/{slice_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return PolicyRead.model_validate(response.json())


async def setup_upf_tunnel(payload: UPFSessionCreate) -> UPFSessionRead:
    async with httpx.AsyncClient(base_url=settings.upf_base_url, timeout=5.0) as client:
        response = await client.post("/upf/setup-tunnel", json=payload.model_dump())
        response.raise_for_status()
        return UPFSessionRead.model_validate(response.json())
