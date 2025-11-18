from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.smf.crud.session import create_session, list_sessions, update_session_status, get_session
from backend.smf.models.session import SessionStatus
from backend.smf.schemas.session import PDUSessionRead, SessionCreateRequest
from backend.smf.services.clients import fetch_policy_for_slice, request_slice_selection, setup_upf_tunnel
from backend.upf.schemas.session import UPFSessionCreate


async def orchestrate_pdu_session(
    payload: SessionCreateRequest,
    session: AsyncSession,
) -> PDUSessionRead:
    slice_resp = await request_slice_selection(payload.requested_slice)

    policy = await fetch_policy_for_slice(slice_resp.slice_id)
    max_bw = policy.max_bandwidth if policy else 100
    qos_profile = policy.qos_profile if policy else "standard"

    pdu_session = await create_session(session=session, payload=payload, slice_id=slice_resp.slice_id)

    try:\n        upf_response = await setup_upf_tunnel(
            UPFSessionCreate(
                pdu_session_id=pdu_session.id,
                ue_id=payload.ue_id,
                slice_id=slice_resp.slice_id,
                qos_profile=qos_profile,
                max_bandwidth=max_bw,
            )
        )
    except Exception as exc:
        await update_session_status(
            session=session,
            session_id=pdu_session.id,
            status=SessionStatus.FAILED,
        )
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="UPF setup failed") from exc

    updated_session = await update_session_status(
        session=session,
        session_id=pdu_session.id,
        status=SessionStatus.ACTIVE,
        upf_session_id=upf_response.id,
    )

    if not updated_session:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Session update failed")

    return PDUSessionRead.model_validate(updated_session)


async def get_session_read(session: AsyncSession, session_id: str) -> PDUSessionRead:
    pdu_session = await get_session(session=session, session_id=session_id)
    if not pdu_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return PDUSessionRead.model_validate(pdu_session)


async def list_session_reads(session: AsyncSession) -> list[PDUSessionRead]:
    sessions = await list_sessions(session=session)
    return [PDUSessionRead.model_validate(pdu_session) for pdu_session in sessions]
