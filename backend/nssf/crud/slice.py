from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.nssf.models.slice import NetworkSlice
from backend.nssf.schemas.slice import SliceCreate


async def create_slice(session: AsyncSession, payload: SliceCreate) -> NetworkSlice:
    slice_obj = NetworkSlice(**payload.model_dump())
    session.add(slice_obj)
    await session.commit()
    await session.refresh(slice_obj)
    return slice_obj


async def list_slices(session: AsyncSession) -> Sequence[NetworkSlice]:
    result = await session.execute(select(NetworkSlice))
    return result.scalars().all()


async def get_slice_by_id(session: AsyncSession, slice_id: str) -> NetworkSlice | None:
    result = await session.execute(select(NetworkSlice).where(NetworkSlice.slice_id == slice_id))
    return result.scalar_one_or_none()
