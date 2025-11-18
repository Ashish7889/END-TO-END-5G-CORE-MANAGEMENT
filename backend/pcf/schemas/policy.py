from __future__ import annotations

from pydantic import BaseModel, Field


class PolicyBase(BaseModel):
    ue_id: str | None = Field(default=None, max_length=64)
    slice_id: str | None = Field(default=None, max_length=64)
    max_bandwidth: int = Field(default=100, ge=1)
    qos_profile: str | None = Field(default=None, max_length=128)


class PolicyCreate(PolicyBase):
    pass


class PolicyRead(PolicyBase):
    id: str

    class Config:
        from_attributes = True
