from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.pcf.models.policy import Policy
from backend.pcf.schemas.policy import PolicyCreate


async def create_policy(session: AsyncSession, payload: PolicyCreate) -> Policy:
    policy = Policy(**payload.model_dump())
    session.add(policy)
    await session.commit()
    await session.refresh(policy)
    return policy


async def list_policies(session: AsyncSession) -> Sequence[Policy]:
    result = await session.execute(select(Policy))
    return result.scalars().all()


async def get_policies_for_ue(session: AsyncSession, ue_id: str) -> Sequence[Policy]:
    result = await session.execute(select(Policy).where(Policy.ue_id == ue_id))
    return result.scalars().all()


async def get_policy_for_slice(session: AsyncSession, slice_id: str) -> Policy | None:
    result = await session.execute(select(Policy).where(Policy.slice_id == slice_id))
    return result.scalar_one_or_none()


async def get_policy_by_id(session: AsyncSession, policy_id: str) -> Policy | None:
    result = await session.execute(select(Policy).where(Policy.id == policy_id))
    return result.scalar_one_or_none()
