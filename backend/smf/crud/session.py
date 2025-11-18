from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.smf.models.session import PDUSession, SessionStatus
from backend.smf.schemas.session import SessionCreateRequest


async def create_session(
    session: AsyncSession,
    payload: SessionCreateRequest,
    slice_id: str,
    upf_session_id: str | None = None,
    status: SessionStatus = SessionStatus.CREATING,
) -> PDUSession:
    pdu_session = PDUSession(
        ue_id=payload.ue_id,
        dnn=payload.dnn,
        slice_id=slice_id,
        upf_session_id=upf_session_id,
        status=status,
    )
    session.add(pdu_session)
    await session.commit()
    await session.refresh(pdu_session)
    return pdu_session


async def update_session_status(
    session: AsyncSession, session_id: str, status: SessionStatus, upf_session_id: str | None = None
) -> PDUSession | None:
    result = await session.execute(select(PDUSession).where(PDUSession.id == session_id))
    pdu_session = result.scalar_one_or_none()
    if not pdu_session:
        return None

    pdu_session.status = status
    if upf_session_id:
        pdu_session.upf_session_id = upf_session_id

    await session.commit()
    await session.refresh(pdu_session)
    return pdu_session


async def get_session(session: AsyncSession, session_id: str) -> PDUSession | None:
    result = await session.execute(select(PDUSession).where(PDUSession.id == session_id))
    return result.scalar_one_or_none()


async def list_sessions(session: AsyncSession) -> Sequence[PDUSession]:
    result = await session.execute(select(PDUSession))
    return result.scalars().all()
