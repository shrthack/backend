import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..infra.db import db_session
from ..cases import points
from ..entities.points import Error, Point, UpsertPoints

router = APIRouter(prefix="/points")


@router.post("/upsert", responses={400: {"model": Error}})
async def upsert_points(
    body: UpsertPoints,
    session: AsyncSession = Depends(db_session),
) -> Point | None:
    dto = await points.upsert_points(session, body.user_id, body.points)
    if dto is None:
        raise HTTPException(status_code=400, detail="Failed to upsert points")
    return Point(user_id=dto.user_id, total_points=dto.total_points)


@router.get("/{user_id}", responses={404: {"model": Error}})
async def get_points(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Point | None:
    dto = await points.get_points(session, user_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Points not found")
    return Point(user_id=dto.user_id, total_points=dto.total_points)