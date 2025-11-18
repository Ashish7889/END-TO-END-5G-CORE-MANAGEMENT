from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.udm_ausf.models.subscriber import Subscriber
from backend.udm_ausf.schemas.subscriber import SubscriberCreate


async def create_subscriber(session: AsyncSession, payload: SubscriberCreate) -> Subscriber:
    subscriber = Subscriber(**payload.model_dump())
    session.add(subscriber)
    await session.commit()
    await session.refresh(subscriber)
    return subscriber


async def get_subscriber_by_imsi(session: AsyncSession, imsi: str) -> Subscriber | None:
    result = await session.execute(select(Subscriber).where(Subscriber.imsi == imsi))
    return result.scalar_one_or_none()


async def list_subscribers(session: AsyncSession) -> Sequence[Subscriber]:
    result = await session.execute(select(Subscriber))
    return result.scalars().all()
