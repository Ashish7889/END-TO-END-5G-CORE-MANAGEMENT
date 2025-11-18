from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class UPFSession(TimestampMixin, Base):
    __tablename__ = "upf_session"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    pdu_session_id: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)
    ue_id: Mapped[str] = mapped_column(String(length=64), nullable=False)
    slice_id: Mapped[str] = mapped_column(String(length=64), nullable=False)
    qos_profile: Mapped[str | None] = mapped_column(String(length=128), nullable=True)
    max_bandwidth: Mapped[int] = mapped_column(Integer, default=100)
    teid: Mapped[str] = mapped_column(String(length=64), unique=True)
    bytes_tx: Mapped[int] = mapped_column(Integer, default=0)
    bytes_rx: Mapped[int] = mapped_column(Integer, default=0)
    packets_tx: Mapped[int] = mapped_column(Integer, default=0)
    packets_rx: Mapped[int] = mapped_column(Integer, default=0)
