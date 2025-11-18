from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from backend.nssf.crud.slice import get_slice_by_id, list_slices
from backend.nssf.schemas.slice import SliceSelectionRequest, SliceSelectionResponse


async def select_slice(
    session: AsyncSession, payload: SliceSelectionRequest
) -> SliceSelectionResponse:
    preferred_slice_id = payload.requested_sst or payload.ue_profile
    if preferred_slice_id:
        slice_obj = await get_slice_by_id(session=session, slice_id=preferred_slice_id)
        if slice_obj:
            return SliceSelectionResponse(
                slice_id=slice_obj.slice_id,
                sst=slice_obj.sst,
                sd=slice_obj.sd,
                description=slice_obj.description,
            )

    slices = await list_slices(session=session)
    if not slices:
        raise ValueError("No slices configured")

    # Simple heuristic: pick first slice (could be improved later)
    slice_obj = slices[0]
    return SliceSelectionResponse(
        slice_id=slice_obj.slice_id,
        sst=slice_obj.sst,
        sd=slice_obj.sd,
        description=slice_obj.description,
    )
