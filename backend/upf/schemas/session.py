from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UPFSessionCreate(BaseModel):
    pdu_session_id: str = Field(..., max_length=64)
    ue_id: str = Field(..., max_length=64)
    slice_id: str = Field(..., max_length=64)
    qos_profile: str | None = Field(default=None, max_length=128)
    max_bandwidth: int = Field(default=100, ge=1)


class UPFSessionRead(UPFSessionCreate):
    id: str
    teid: str
    bytes_tx: int
    bytes_rx: int
    packets_tx: int
    packets_rx: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UPFMetrics(BaseModel):
    total_sessions: int
    total_bytes_tx: int
    total_bytes_rx: int
    total_packets_tx: int
    total_packets_rx: int
