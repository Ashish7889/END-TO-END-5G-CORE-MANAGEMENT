from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class Policy(TimestampMixin, Base):
    __tablename__ = "policy"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    ue_id: Mapped[str | None] = mapped_column(String(length=64), nullable=True, index=True)
    slice_id: Mapped[str | None] = mapped_column(String(length=64), nullable=True, index=True)
    max_bandwidth: Mapped[int] = mapped_column(Integer, default=100)
    qos_profile: Mapped[str | None] = mapped_column(String(length=128), nullable=True)
