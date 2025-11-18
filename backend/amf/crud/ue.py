from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.amf.models.ue import UE, UEState
from backend.amf.schemas.ue import UECreateRequest


async def create_or_update_ue(
    session: AsyncSession, payload: UECreateRequest, slice_id: str | None = None
) -> UE:
    result = await session.execute(select(UE).where(UE.ue_id == payload.ue_id))
    ue = result.scalar_one_or_none()

    if ue:
        ue.last_seen = datetime.utcnow()
        if slice_id:
            ue.slice_id = slice_id
        ue.state = UEState.REGISTERED
    else:
        ue = UE(
            ue_id=payload.ue_id,
            imsi=payload.imsi,
            state=UEState.REGISTERED,
            slice_id=slice_id,
        )
        session.add(ue)

    await session.commit()
    await session.refresh(ue)
    return ue


async def get_ue_by_id(session: AsyncSession, ue_id: str) -> UE | None:
    result = await session.execute(select(UE).where(UE.ue_id == ue_id))
    return result.scalar_one_or_none()


async def list_ues(session: AsyncSession) -> Sequence[UE]:
    result = await session.execute(select(UE))
    return result.scalars().all()
