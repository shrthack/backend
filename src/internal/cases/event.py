import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db import event as e
from db import models as m
from ..entities.event import (
    CreateEvent,
    UpdateEvent,
)


async def create_event(conn: AsyncSession, ent: CreateEvent) -> m.Event | None:
    async with conn.begin():
        q = e.AsyncQuerier(await conn.connection())
        event = await q.create_event(**ent.to_params())
        return event


async def get_event(conn: AsyncSession, id: uuid.UUID) -> m.Event | None:
    async with conn.begin():
        q = e.AsyncQuerier(await conn.connection())
        event = await q.get_event_by_id(id=id)
        return event


async def get_all_events(conn: AsyncSession):
    async with conn.begin():
        q = e.AsyncQuerier(await conn.connection())
        async for event in q.get_all_events():
            yield event


async def update_event(
    conn: AsyncSession, id: uuid.UUID, ent: UpdateEvent
) -> m.Event | None:
    async with conn.begin():
        q = e.AsyncQuerier(await conn.connection())
        event = await q.update_event(ent.to_params(id))
        return event


async def delete_event(conn: AsyncSession, id: uuid.UUID) -> bool:
    async with conn.begin():
        q = e.AsyncQuerier(await conn.connection())
        await q.delete_event(id=id)
        return True

