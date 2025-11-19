from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PDUSessionTimeline(BaseModel):
    session_id: int = Field(..., description="PDU Session ID")
    ue_id: str = Field(..., description="UE identifier")
    slice: str = Field(..., description="Network slice")
    start: datetime = Field(..., description="Session start time")
    end: Optional[datetime] = Field(None, description="Session end time (null if active)")
    qos: int = Field(..., description="QoS level")
    upf_node: str = Field(..., description="UPF node handling the session")

class PDUSessionTimelineList(BaseModel):
    sessions: List[PDUSessionTimeline]
