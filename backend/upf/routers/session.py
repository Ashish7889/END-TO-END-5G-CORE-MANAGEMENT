from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.db import get_async_session
from backend.upf.crud.upf_session import aggregate_metrics, create_upf_session, list_upf_sessions
from backend.upf.schemas.session import UPFMetrics, UPFSessionCreate, UPFSessionRead

router = APIRouter(prefix="/upf", tags=["upf"])


@router.post("/setup-tunnel", response_model=UPFSessionRead, status_code=status.HTTP_201_CREATED)
async def setup_tunnel(
    payload: UPFSessionCreate, session: AsyncSession = Depends(get_async_session)
) -> UPFSessionRead:
    upf_session = await create_upf_session(session=session, payload=payload)
    return UPFSessionRead.model_validate(upf_session)


@router.get("/sessions", response_model=list[UPFSessionRead])
async def get_upf_sessions(session: AsyncSession = Depends(get_async_session)) -> list[UPFSessionRead]:
    sessions = await list_upf_sessions(session=session)
    return [UPFSessionRead.model_validate(upf_session) for upf_session in sessions]


@router.get("/metrics", response_model=UPFMetrics)
async def get_metrics(session: AsyncSession = Depends(get_async_session)) -> UPFMetrics:
    return await aggregate_metrics(session=session)
