from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class UEState(StrEnum):
    REGISTERED = "REGISTERED"
    DEREGISTERED = "DEREGISTERED"
    REJECTED = "REJECTED"


class UE(TimestampMixin, Base):
    __tablename__ = "ue"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    ue_id: Mapped[str] = mapped_column(String(length=64), unique=True, index=True)
    imsi: Mapped[str] = mapped_column(String(length=32), unique=True, index=True)
    state: Mapped[UEState] = mapped_column(Enum(UEState, name="ue_state"), default=UEState.DEREGISTERED)
    slice_id: Mapped[str | None] = mapped_column(String(length=32), nullable=True)
    last_seen: Mapped[datetime] = mapped_column(default=datetime.utcnow)
