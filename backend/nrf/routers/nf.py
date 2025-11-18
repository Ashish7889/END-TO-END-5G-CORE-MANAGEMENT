from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.db import get_async_session
from backend.nrf import models
from backend.nrf.crud import nf as nf_crud
from backend.nrf.schemas import NFRegisterRequest, NetworkFunctionRead

router = APIRouter(prefix="/nrf", tags=["nrf"])


@router.post("/register-nf", response_model=NetworkFunctionRead, status_code=status.HTTP_201_CREATED)
async def register_nf(
    payload: NFRegisterRequest, session: AsyncSession = Depends(get_async_session)
) -> NetworkFunctionRead:
    nf = await nf_crud.register_or_update_nf(session=session, payload=payload)
    return NetworkFunctionRead.model_validate(nf)


@router.get("/nfs", response_model=list[NetworkFunctionRead])
async def get_all_nfs(session: AsyncSession = Depends(get_async_session)) -> list[NetworkFunctionRead]:
    nfs = await nf_crud.list_nfs(session=session)
    return [NetworkFunctionRead.model_validate(nf) for nf in nfs]


@router.get("/nfs/{nf_type}", response_model=list[NetworkFunctionRead])
async def get_nfs_by_type(
    nf_type: models.NFType, session: AsyncSession = Depends(get_async_session)
) -> list[NetworkFunctionRead]:
    nfs = await nf_crud.list_nfs_by_type(session=session, nf_type=nf_type)
    return [NetworkFunctionRead.model_validate(nf) for nf in nfs]
