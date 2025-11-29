import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..infra.db import db_session
from ..cases import stand
from ..entities.stand import (
    Stand,
    CreateStand,
    UpdateStand,
    Error,
)

router = APIRouter(prefix="/stands")


@router.post("", responses={400: {"model": Error}})
async def create_stand(
    body: CreateStand,
    session: AsyncSession = Depends(db_session),
) -> Stand | None | Error:
    try:
        dto = await stand.create_stand(session, body)
        assert dto is not None
        return Stand(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            location=dto.location,
            image_url=dto.image_url,
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Stand creation failed")


@router.get("", response_model=list[Stand])
async def get_all_stands(
    session: AsyncSession = Depends(db_session),
):
    stands = []
    async for dto in stand.get_all_stands(session):
        stands.append(Stand(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            location=dto.location,
            image_url=dto.image_url,
        ))
    return stands


@router.get("/{id}", responses={404: {"model": Error}})
async def get_stand(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Stand | None:
    try:
        dto = await stand.get_stand(session, id)
        if dto is None:
            raise HTTPException(status_code=404, detail="Stand not found")
        return Stand(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            location=dto.location,
            image_url=dto.image_url,
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Stand not found")


@router.put("/{id}", responses={404: {"model": Error}})
async def update_stand(
    id: uuid.UUID,
    ent: UpdateStand,
    session: AsyncSession = Depends(db_session),
) -> Stand | None:
    dto = await stand.update_stand(session, id, ent)
    if dto is None:
        raise HTTPException(status_code=404, detail="Stand not found")
    return Stand(
        id=dto.id,
        name=dto.name,
        info=dto.info,
        location=dto.location,
        image_url=dto.image_url,
    )


@router.delete("/{id}", responses={204: {}, 404: {"model": Error}})
async def delete_stand(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Response:
    if await stand.delete_stand(session, id):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Stand not found")