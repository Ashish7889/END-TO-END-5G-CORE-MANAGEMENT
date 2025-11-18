from __future__ import annotations

from pydantic import BaseModel, Field


class UEAuthRequest(BaseModel):
    imsi: str = Field(..., max_length=32)
    key: str = Field(..., max_length=128)


class UEAuthResponse(BaseModel):
    success: bool
    message: str
    ue_profile: str | None = None
    slice_preference: str | None = None
