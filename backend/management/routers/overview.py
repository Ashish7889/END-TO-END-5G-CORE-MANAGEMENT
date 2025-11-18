from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.management.dependencies.api_key import api_key_dependency
from backend.management.schemas.models import OverviewMetrics, SessionInfo, UEInfo
from backend.management.services.aggregator import (
    build_overview,
    collect_sessions,
    collect_ues,
    summarize_nfs,
)

router = APIRouter(prefix="/mgmt", tags=["management"], dependencies=[Depends(api_key_dependency)])


@router.get("/overview", response_model=OverviewMetrics)
async def get_overview() -> OverviewMetrics:
    return await build_overview()


@router.get("/ues", response_model=list[UEInfo])
async def get_ues() -> list[UEInfo]:
    return await collect_ues()


@router.get("/sessions", response_model=list[SessionInfo])
async def get_sessions() -> list[SessionInfo]:
    return await collect_sessions()


@router.get("/nfs-status")
async def get_nfs_status() -> dict:
    return await summarize_nfs()
