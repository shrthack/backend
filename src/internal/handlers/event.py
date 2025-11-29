import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..infra.db import db_session
from ..cases import event
from ..entities.event import (
    Event,
    CreateEvent,
    UpdateEvent,
    Error,
)

router = APIRouter(prefix="/events")


@router.post("", responses={400: {"model": Error}})
async def create_event(
    body: CreateEvent,
    session: AsyncSession = Depends(db_session),
) -> Event | None | Error:
    try:
        dto = await event.create_event(session, body)
        assert dto is not None
        return Event(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            image_url=dto.image_url,
            points=dto.points,
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Event creation failed")


@router.get("", response_model=list[Event])
async def get_all_events(
    session: AsyncSession = Depends(db_session),
):
    events = []
    async for dto in event.get_all_events(session):
        events.append(Event(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            image_url=dto.image_url,
            points=dto.points,
        ))
    return events


@router.get("/{id}", responses={404: {"model": Error}})
async def get_event(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Event | None:
    try:
        dto = await event.get_event(session, id)
        if dto is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return Event(
            id=dto.id,
            name=dto.name,
            info=dto.info,
            image_url=dto.image_url,
            points=dto.points,
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Event not found")


@router.put("/{id}", responses={404: {"model": Error}})
async def update_event(
    id: uuid.UUID,
    ent: UpdateEvent,
    session: AsyncSession = Depends(db_session),
) -> Event | None:
    dto = await event.update_event(session, id, ent)
    if dto is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event(
        id=dto.id,
        name=dto.name,
        info=dto.info,
        image_url=dto.image_url,
        points=dto.points,
    )


@router.delete("/{id}", responses={204: {}, 404: {"model": Error}})
async def delete_event(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Response:
    if await event.delete_event(session, id):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Event not found")