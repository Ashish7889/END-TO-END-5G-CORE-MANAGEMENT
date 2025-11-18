from __future__ import annotations

from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.models_base import Base, TimestampMixin


class Subscriber(TimestampMixin, Base):
    __tablename__ = "subscriber"

    id: Mapped[str] = mapped_column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    imsi: Mapped[str] = mapped_column(String(length=32), unique=True, nullable=False, index=True)
    auth_key: Mapped[str] = mapped_column(String(length=128), nullable=False)
    slice_preference: Mapped[str | None] = mapped_column(String(length=32), nullable=True)
    ue_profile: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
