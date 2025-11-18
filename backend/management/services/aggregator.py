from __future__ import annotations

from collections import Counter

from backend.management.schemas.models import (
    NFStatusSummary,
    NetworkFunctionInfo,
    OverviewMetrics,
    SessionInfo,
    SliceBreakdown,
    UEInfo,
)
from backend.management.services.clients import fetch_nfs, fetch_sessions, fetch_upf_metrics, fetch_ues


async def collect_ues() -> list[UEInfo]:
    raw = await fetch_ues()
    return [UEInfo.model_validate(item) for item in raw]


async def collect_sessions() -> list[SessionInfo]:
    raw = await fetch_sessions()
    return [SessionInfo.model_validate(item) for item in raw]


async def collect_nfs() -> list[NetworkFunctionInfo]:
    raw = await fetch_nfs()
    return [NetworkFunctionInfo.model_validate(item) for item in raw]


async def build_overview() -> OverviewMetrics:
    ues, sessions, nfs, upf_metrics = await _gather_all()

    registered_ues = sum(1 for ue in ues if ue.state == "REGISTERED")
    active_sessions = sum(1 for sess in sessions if sess.status == "ACTIVE")
    slice_counts = Counter(sess.slice_id for sess in sessions)

    slice_distribution = [
        SliceBreakdown(slice_id=slice_id, session_count=count)
        for slice_id, count in slice_counts.items()
    ]

    nf_up = sum(1 for nf in nfs if nf.status == "UP")
    nf_status = NFStatusSummary(total=len(nfs), up=nf_up, down=len(nfs) - nf_up)

    return OverviewMetrics(
        total_ues=len(ues),
        registered_ues=registered_ues,
        total_sessions=len(sessions),
        active_sessions=active_sessions,
        slice_distribution=slice_distribution,
        nf_status=nf_status,
        upf_metrics=upf_metrics,
    )


async def _gather_all():
    from asyncio import gather

    return await gather(collect_ues(), collect_sessions(), collect_nfs(), fetch_upf_metrics())


async def summarize_nfs() -> dict:
    nfs = await collect_nfs()
    return {
        "nfs": [nf.model_dump() for nf in nfs],
        "summary": {
            "total": len(nfs),
            "up": sum(1 for nf in nfs if nf.status == "UP"),
            "down": sum(1 for nf in nfs if nf.status != "UP"),
        },
    }
