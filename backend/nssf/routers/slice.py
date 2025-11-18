from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.db import get_async_session
from backend.nssf.crud.slice import create_slice, list_slices
from backend.nssf.schemas.slice import (
    SliceCreate,
    SliceRead,
    SliceSelectionRequest,
    SliceSelectionResponse,
)
from backend.nssf.services.selection import select_slice

router = APIRouter(prefix="/nssf", tags=["nssf"])


@router.post("/slices", response_model=SliceRead, status_code=status.HTTP_201_CREATED)
async def create_slice_endpoint(
    payload: SliceCreate, session: AsyncSession = Depends(get_async_session)
) -> SliceRead:
    slice_obj = await create_slice(session=session, payload=payload)
    return SliceRead.model_validate(slice_obj)


@router.get("/slices", response_model=list[SliceRead])
async def list_slices_endpoint(
    session: AsyncSession = Depends(get_async_session),
) -> list[SliceRead]:
    slices = await list_slices(session=session)
    return [SliceRead.model_validate(slice_obj) for slice_obj in slices]


@router.post("/select-slice", response_model=SliceSelectionResponse)
async def select_slice_endpoint(
    payload: SliceSelectionRequest, session: AsyncSession = Depends(get_async_session)
) -> SliceSelectionResponse:
    try:
        return await select_slice(session=session, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
