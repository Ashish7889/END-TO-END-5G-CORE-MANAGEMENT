from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from backend.smf.models.session import SessionStatus


class SessionCreateRequest(BaseModel):
    ue_id: str = Field(..., max_length=64)
    dnn: str = Field(..., max_length=64)
    requested_slice: str | None = Field(default=None)


class PDUSessionRead(BaseModel):
    id: str
    ue_id: str
    dnn: str
    slice_id: str
    upf_session_id: str | None
    status: SessionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
