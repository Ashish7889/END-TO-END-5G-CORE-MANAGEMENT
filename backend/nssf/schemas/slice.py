from __future__ import annotations

from pydantic import BaseModel, Field


class SliceBase(BaseModel):
    slice_id: str = Field(..., max_length=64)
    description: str | None = Field(default=None, max_length=256)
    sst: str = Field(..., max_length=16)
    sd: str | None = Field(default=None, max_length=16)


class SliceCreate(SliceBase):
    pass


class SliceRead(SliceBase):
    id: str

    class Config:
        from_attributes = True


class SliceSelectionRequest(BaseModel):
    ue_profile: str | None = None
    dnn: str | None = None
    requested_sst: str | None = None


class SliceSelectionResponse(BaseModel):
    slice_id: str
    sst: str
    sd: str | None = None
    description: str | None = None
