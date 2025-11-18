from __future__ import annotations

from random import randint
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.upf.models.session import UPFSession
from backend.upf.schemas.session import UPFSessionCreate, UPFMetrics


async def create_upf_session(session: AsyncSession, payload: UPFSessionCreate) -> UPFSession:
    upf_session = UPFSession(
        **payload.model_dump(),
        teid=f"TEID-{randint(10000, 99999)}",
        bytes_tx=randint(10_000, 50_000),
        bytes_rx=randint(10_000, 50_000),
        packets_tx=randint(500, 2000),
        packets_rx=randint(500, 2000),
    )
    session.add(upf_session)
    await session.commit()
    await session.refresh(upf_session)
    return upf_session


async def list_upf_sessions(session: AsyncSession) -> Sequence[UPFSession]:
    result = await session.execute(select(UPFSession))
    return result.scalars().all()


async def aggregate_metrics(session: AsyncSession) -> UPFMetrics:
    result = await session.execute(
        select(
            func.count(UPFSession.id),
            func.coalesce(func.sum(UPFSession.bytes_tx), 0),
            func.coalesce(func.sum(UPFSession.bytes_rx), 0),
            func.coalesce(func.sum(UPFSession.packets_tx), 0),
            func.coalesce(func.sum(UPFSession.packets_rx), 0),
        )
    )
    total_sessions, bytes_tx, bytes_rx, packets_tx, packets_rx = result.one()
    return UPFMetrics(
        total_sessions=total_sessions or 0,
        total_bytes_tx=bytes_tx or 0,
        total_bytes_rx=bytes_rx or 0,
        total_packets_tx=packets_tx or 0,
        total_packets_rx=packets_rx or 0,
    )
