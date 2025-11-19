from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LogEntry(BaseModel):
    timestamp: datetime = Field(..., description="Log timestamp")
    level: str = Field(..., description="Log level (INFO, WARNING, ERROR)")
    message: str = Field(..., description="Log message")
    source: str = Field(..., description="Log source component")

class LogList(BaseModel):
    logs: List[LogEntry]
