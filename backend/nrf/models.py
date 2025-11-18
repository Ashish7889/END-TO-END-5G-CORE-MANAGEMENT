from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class NFType(StrEnum):
    AMF = "AMF"
    SMF = "SMF"
    UPF = "UPF"
    NRF = "NRF"
    NSSF = "NSSF"
    PCF = "PCF"
    UDM = "UDM"
    AUSF = "AUSF"


class NFStatus(StrEnum):
    UP = "UP"
    DOWN = "DOWN"


class NetworkFunction(TimestampMixin, Base):
    __tablename__ = "network_function"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    nf_type: Mapped[NFType] = mapped_column(Enum(NFType, name="nf_type"), nullable=False)
    name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(length=256), nullable=False)
    status: Mapped[NFStatus] = mapped_column(Enum(NFStatus, name="nf_status"), default=NFStatus.UP)
    last_heartbeat: Mapped[datetime] = mapped_column(default=datetime.utcnow)
