from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.db import get_async_session
from backend.smf.schemas.session import PDUSessionRead, SessionCreateRequest
from backend.smf.services.manager import (
    get_session_read,
    list_session_reads,
    orchestrate_pdu_session,
)

router = APIRouter(prefix="/smf", tags=["smf"])


@router.post("/sessions", response_model=PDUSessionRead)
async def create_pdu_session(
    payload: SessionCreateRequest, session: AsyncSession = Depends(get_async_session)
) -> PDUSessionRead:
    return await orchestrate_pdu_session(payload=payload, session=session)


@router.get("/sessions", response_model=list[PDUSessionRead])
async def get_sessions(session: AsyncSession = Depends(get_async_session)) -> list[PDUSessionRead]:
    return await list_session_reads(session=session)


@router.get("/sessions/{session_id}", response_model=PDUSessionRead)
async def get_session_endpoint(
    session_id: str, session: AsyncSession = Depends(get_async_session)
) -> PDUSessionRead:
    return await get_session_read(session=session, session_id=session_id)
