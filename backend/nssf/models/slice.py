from __future__ import annotations

from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class NetworkSlice(TimestampMixin, Base):
    __tablename__ = "network_slice"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    slice_id: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    sst: Mapped[str] = mapped_column(String(length=16), nullable=False)
    sd: Mapped[str | None] = mapped_column(String(length=16), nullable=True)
