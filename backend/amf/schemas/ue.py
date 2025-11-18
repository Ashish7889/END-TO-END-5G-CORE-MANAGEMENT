from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from backend.amf.models.ue import UEState


class UEBase(BaseModel):
    ue_id: str = Field(..., max_length=64)
    imsi: str = Field(..., max_length=32)


class UECreateRequest(UEBase):
    auth_key: str = Field(..., max_length=128, description="Key used for authentication with UDM/AUSF")


class UERead(UEBase):
    id: str
    state: UEState
    slice_id: str | None = None
    last_seen: datetime

    class Config:
        from_attributes = True
