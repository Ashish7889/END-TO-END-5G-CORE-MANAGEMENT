from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.db import get_async_session
from backend.pcf.crud.policy import (
    create_policy,
    get_policy_by_id,
    get_policy_for_slice,
    get_policies_for_ue,
    list_policies,
)
from backend.pcf.schemas.policy import PolicyCreate, PolicyRead

router = APIRouter(prefix="/pcf", tags=["pcf"])


@router.post("/policies", response_model=PolicyRead, status_code=status.HTTP_201_CREATED)
async def create_policy_endpoint(
    payload: PolicyCreate, session: AsyncSession = Depends(get_async_session)
) -> PolicyRead:
    policy = await create_policy(session=session, payload=payload)
    return PolicyRead.model_validate(policy)


@router.get("/policies", response_model=list[PolicyRead])
async def list_policies_endpoint(session: AsyncSession = Depends(get_async_session)) -> list[PolicyRead]:
    policies = await list_policies(session=session)
    return [PolicyRead.model_validate(policy) for policy in policies]


@router.get("/policies/ue/{ue_id}", response_model=list[PolicyRead])
async def get_policies_for_ue_endpoint(
    ue_id: str, session: AsyncSession = Depends(get_async_session)
) -> list[PolicyRead]:
    policies = await get_policies_for_ue(session=session, ue_id=ue_id)
    return [PolicyRead.model_validate(policy) for policy in policies]


@router.get("/policies/slice/{slice_id}", response_model=PolicyRead)
async def get_policy_for_slice_endpoint(
    slice_id: str, session: AsyncSession = Depends(get_async_session)
) -> PolicyRead:
    policy = await get_policy_for_slice(session=session, slice_id=slice_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return PolicyRead.model_validate(policy)


@router.get("/policies/{policy_id}", response_model=PolicyRead)
async def get_policy_by_id_endpoint(
    policy_id: str, session: AsyncSession = Depends(get_async_session)
) -> PolicyRead:
    policy = await get_policy_by_id(session=session, policy_id=policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return PolicyRead.model_validate(policy)
