from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.nrf import models
from backend.nrf.schemas import NFRegisterRequest


async def register_or_update_nf(session: AsyncSession, payload: NFRegisterRequest) -> models.NetworkFunction:
    stmt = select(models.NetworkFunction).where(
        (models.NetworkFunction.nf_type == payload.nf_type)
        & (models.NetworkFunction.name == payload.name)
    )
    result = await session.execute(stmt)
    nf: models.NetworkFunction | None = result.scalar_one_or_none()

    if nf:
        nf.endpoint = str(payload.endpoint)
        nf.status = payload.status
        nf.last_heartbeat = datetime.utcnow()
    else:
        nf = models.NetworkFunction(
            nf_type=payload.nf_type,
            name=payload.name,
            endpoint=str(payload.endpoint),
            status=payload.status,
            last_heartbeat=datetime.utcnow(),
        )
        session.add(nf)

    await session.commit()
    await session.refresh(nf)
    return nf


async def list_nfs(session: AsyncSession) -> Sequence[models.NetworkFunction]:
    result = await session.execute(select(models.NetworkFunction))
    return result.scalars().all()


async def list_nfs_by_type(
    session: AsyncSession, nf_type: models.NFType
) -> Sequence[models.NetworkFunction]:
    result = await session.execute(
        select(models.NetworkFunction).where(models.NetworkFunction.nf_type == nf_type)
    )
    return result.scalars().all()


async def get_nf_by_id(session: AsyncSession, nf_id: UUID) -> models.NetworkFunction | None:
    result = await session.execute(
        select(models.NetworkFunction).where(models.NetworkFunction.id == nf_id)
    )
    return result.scalar_one_or_none()
