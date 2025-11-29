import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..infra.db import db_session
from ..cases import merch
from ..entities.merch import (
    Merch,
    CreateMerch,
    Error,
    UpdateMerch,
)

router = APIRouter(prefix="/merch")


@router.post("/", responses={400: {"model": Error}})
async def create_merch(
    body: CreateMerch,
    session: AsyncSession = Depends(db_session),
) -> Merch | None | Error:
    try:
        dto = await merch.create(session, body)
        assert dto is not None
        return Merch(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            image_url=dto.image_url,
            points_needed=dto.points_needed,
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Merch already exists")


@router.get("/", responses={200: {"model": list[Merch]}})
async def get_all_merch(
    session: AsyncSession = Depends(db_session),
) -> list[Merch]:
    dtos = await merch.get_all(session)
    return [
        Merch(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            image_url=dto.image_url,
            points_needed=dto.points_needed,
        )
        for dto in dtos
    ]


@router.get("/{id}", responses={404: {"model": Error}})
async def get_merch(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Merch | None:
    try:
        dto = await merch.get(session, id)
        if dto is None:
            raise HTTPException(status_code=404, detail="Merch not found")
        return Merch(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            image_url=dto.image_url,
            points_needed=dto.points_needed,
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Merch not found")


@router.put("/{id}", responses={404: {"model": Error}})
async def update_merch(
    id: uuid.UUID,
    ent: UpdateMerch,
    session: AsyncSession = Depends(db_session),
) -> Merch | None:
    dto = await merch.update(session, id, ent)
    if dto is None:
        raise HTTPException(status_code=404, detail="Merch not found")
    return Merch(
        id=dto.id,
        name=dto.name,
        info=dto.info,
        image_url=dto.image_url,
        points_needed=dto.points_needed,
    )


@router.delete("/{id}", responses={204: {}, 404: {"model": Error}})
async def delete_merch(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Response:
    await merch.delete(session, id)
    return Response(status_code=204)