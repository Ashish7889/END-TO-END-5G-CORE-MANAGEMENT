from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class AlertSeverity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class AlertType(str, Enum):
    UE_DETACHED = "UE_DETACHED"
    UPF_FAILURE = "UPF_FAILURE"
    HIGH_LATENCY = "HIGH_LATENCY"
    HIGH_BYTES_USAGE = "HIGH_BYTES_USAGE"
    NF_UNREACHABLE = "NF_UNREACHABLE"

class Alert(BaseModel):
    type: AlertType = Field(..., description="Alert type")
    message: str = Field(..., description="Alert message")
    severity: AlertSeverity = Field(..., description="Alert severity")
    timestamp: datetime = Field(..., description="Alert timestamp")

class AlertList(BaseModel):
    alerts: List[Alert]
