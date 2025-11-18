from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.amf.crud.ue import create_or_update_ue, get_ue_by_id, list_ues
from backend.amf.schemas.ue import UECreateRequest, UERead
from backend.amf.services.auth import authenticate_with_udm
from backend.common.db import get_async_session
from backend.udm_ausf.schemas.auth import UEAuthRequest

router = APIRouter(prefix="/amf", tags=["amf"])


@router.post("/ue/register", response_model=UERead, status_code=status.HTTP_201_CREATED)
async def register_ue(
    payload: UECreateRequest, session: AsyncSession = Depends(get_async_session)
) -> UERead:
    auth_response = await authenticate_with_udm(
        UEAuthRequest(imsi=payload.imsi, key=payload.auth_key)
    )

    if not auth_response.success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=auth_response.message)

    ue = await create_or_update_ue(session=session, payload=payload, slice_id=auth_response.slice_preference)
    return UERead.model_validate(ue)


@router.get("/ue/{ue_id}", response_model=UERead)
async def get_ue(ue_id: str, session: AsyncSession = Depends(get_async_session)) -> UERead:
    ue = await get_ue_by_id(session=session, ue_id=ue_id)
    if not ue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UE not found")
    return UERead.model_validate(ue)


@router.get("/ues", response_model=list[UERead])
async def list_registered_ues(
    session: AsyncSession = Depends(get_async_session),
) -> list[UERead]:
    ues = await list_ues(session=session)
    return [UERead.model_validate(ue) for ue in ues]
