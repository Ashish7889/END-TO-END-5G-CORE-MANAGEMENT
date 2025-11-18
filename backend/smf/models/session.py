from __future__ import annotations

from enum import StrEnum
from uuid import uuid4

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class SessionStatus(StrEnum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


class PDUSession(TimestampMixin, Base):
    __tablename__ = "pdu_session"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    ue_id: Mapped[str] = mapped_column(String(length=64), index=True)
    dnn: Mapped[str] = mapped_column(String(length=64))
    slice_id: Mapped[str] = mapped_column(String(length=64))
    upf_session_id: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, name="session_status"), default=SessionStatus.CREATING
    )
