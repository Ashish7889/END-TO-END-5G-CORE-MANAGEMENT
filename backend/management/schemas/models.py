from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UEInfo(BaseModel):
    id: str
    ue_id: str
    imsi: str
    state: str
    slice_id: str | None = None
    last_seen: datetime


class SessionInfo(BaseModel):
    id: str
    ue_id: str
    dnn: str
    slice_id: str
    upf_session_id: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime


class NetworkFunctionInfo(BaseModel):
    id: str
    nf_type: str
    name: str
    endpoint: str
    status: str
    last_heartbeat: datetime


class NFStatusSummary(BaseModel):
    total: int
    up: int
    down: int


class SliceBreakdown(BaseModel):
    slice_id: str
    session_count: int


class OverviewMetrics(BaseModel):
    total_ues: int
    registered_ues: int
    total_sessions: int
    active_sessions: int
    slice_distribution: list[SliceBreakdown] = Field(default_factory=list)
    nf_status: NFStatusSummary
    upf_metrics: dict[str, int]
