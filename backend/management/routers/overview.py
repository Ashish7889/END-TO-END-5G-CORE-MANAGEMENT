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


@router.get("/slices")
async def get_slices() -> list[dict]:
    """Get slice information from sessions"""
    sessions = await collect_sessions()
    slice_counts = {}
    for session in sessions:
        slice_id = session.slice_id
        if slice_id not in slice_counts:
            slice_counts[slice_id] = {
                "slice_id": slice_id,
                "session_count": 0,
                "active_sessions": 0,
                "ues": set()
            }
        slice_counts[slice_id]["session_count"] += 1
        if session.status == "ACTIVE":
            slice_counts[slice_id]["active_sessions"] += 1
        slice_counts[slice_id]["ues"].add(session.ue_id)
    
    # Convert sets to counts
    result = []
    for slice_data in slice_counts.values():
        result.append({
            "slice_id": slice_data["slice_id"],
            "session_count": slice_data["session_count"],
            "active_sessions": slice_data["active_sessions"],
            "ue_count": len(slice_data["ues"])
        })
    return result
