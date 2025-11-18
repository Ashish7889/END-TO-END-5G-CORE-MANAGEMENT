from __future__ import annotations

from pydantic import BaseModel, Field


class SubscriberBase(BaseModel):
    imsi: str = Field(..., max_length=32)
    auth_key: str = Field(..., max_length=128)
    slice_preference: str | None = Field(default=None)
    ue_profile: str | None = Field(default=None)


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberRead(SubscriberBase):
    id: str

    class Config:
        from_attributes = True
