from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.db import get_async_session
from backend.udm_ausf.crud.subscriber import get_subscriber_by_imsi, list_subscribers
from backend.udm_ausf.schemas.auth import UEAuthRequest, UEAuthResponse
from backend.udm_ausf.schemas.subscriber import SubscriberCreate, SubscriberRead

router = APIRouter(prefix="/auth", tags=["udm-ausf"])


@router.post("/ue-auth", response_model=UEAuthResponse)
async def authenticate_ue(
    payload: UEAuthRequest, session: AsyncSession = Depends(get_async_session)
) -> UEAuthResponse:
    subscriber = await get_subscriber_by_imsi(session=session, imsi=payload.imsi)
    if not subscriber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscriber not found")

    if subscriber.auth_key != payload.key:
        return UEAuthResponse(success=False, message="Authentication failed")

    return UEAuthResponse(
        success=True,
        message="Authentication successful",
        ue_profile=subscriber.ue_profile,
        slice_preference=subscriber.slice_preference,
    )


@router.get("/subscribers", response_model=list[SubscriberRead])
async def get_subscribers(session: AsyncSession = Depends(get_async_session)) -> list[SubscriberRead]:
    subscribers = await list_subscribers(session=session)
    return [SubscriberRead.model_validate(sub) for sub in subscribers]


@router.post("/subscribers", response_model=SubscriberRead, status_code=status.HTTP_201_CREATED)
async def create_subscriber_endpoint(
    payload: SubscriberCreate, session: AsyncSession = Depends(get_async_session)
) -> SubscriberRead:
    subscriber = await get_subscriber_by_imsi(session=session, imsi=payload.imsi)
    if subscriber:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subscriber exists")

    from backend.udm_ausf.crud.subscriber import create_subscriber

    subscriber = await create_subscriber(session=session, payload=payload)
    return SubscriberRead.model_validate(subscriber)
