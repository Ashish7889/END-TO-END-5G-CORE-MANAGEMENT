from __future__ import annotations

import httpx

from backend.common.config import get_settings

settings = get_settings()


async def fetch_ues() -> list[dict]:
    async with httpx.AsyncClient(base_url=settings.amf_base_url, timeout=5.0) as client:
        resp = await client.get("/amf/ues")
        resp.raise_for_status()
        return resp.json()


async def fetch_sessions() -> list[dict]:
    async with httpx.AsyncClient(base_url=settings.smf_base_url, timeout=5.0) as client:
        resp = await client.get("/smf/sessions")
        resp.raise_for_status()
        return resp.json()


async def fetch_nfs() -> list[dict]:
    async with httpx.AsyncClient(base_url=settings.nrf_base_url, timeout=5.0) as client:
        resp = await client.get("/nrf/nfs")
        resp.raise_for_status()
        return resp.json()


async def fetch_upf_metrics() -> dict:
    async with httpx.AsyncClient(base_url=settings.upf_base_url, timeout=5.0) as client:
        resp = await client.get("/upf/metrics")
        resp.raise_for_status()
        return resp.json()
