from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class NFType(str, Enum):
    AMF = "AMF"
    SMF = "SMF"
    UPF = "UPF"
    NRF = "NRF"
    NSSF = "NSSF"
    PCF = "PCF"
    UDM = "UDM"
    AUSF = "AUSF"


class NFStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"


class NFBase(BaseModel):
    nf_type: NFType = Field(..., description="Type of network function")
    name: str = Field(..., max_length=64)
    endpoint: HttpUrl = Field(..., description="Base URL where the NF can be reached")
    status: NFStatus = Field(default=NFStatus.UP)


class NFRegisterRequest(NFBase):
    pass


class NetworkFunctionRead(NFBase):
    id: UUID
    last_heartbeat: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
