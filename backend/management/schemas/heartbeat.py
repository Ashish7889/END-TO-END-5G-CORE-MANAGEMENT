from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class NFStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNREACHABLE = "UNREACHABLE"

class NFHeartbeat(BaseModel):
    name: str = Field(..., description="Network function instance name")
    type: str = Field(..., description="Network function type (AMF, SMF, UPF, etc.)")
    status: NFStatus = Field(..., description="Current status of the NF")
    last_heartbeat: datetime = Field(..., description="Last heartbeat timestamp")
    endpoint: str = Field(..., description="Endpoint IP address")

class NFHeartbeatList(BaseModel):
    heartbeats: List[NFHeartbeat]
