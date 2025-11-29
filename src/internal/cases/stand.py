import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db import stand as s
from db import models as m
from ..entities.stand import (
    CreateStand,
    UpdateStand,
)


async def create_stand(conn: AsyncSession, ent: CreateStand) -> m.Stand | None:
    async with conn.begin():
        q = s.AsyncQuerier(await conn.connection())
        stand = await q.create_stand(**ent.to_params())
        return stand


async def get_stand(conn: AsyncSession, id: uuid.UUID) -> m.Stand | None:
    async with conn.begin():
        q = s.AsyncQuerier(await conn.connection())
        stand = await q.get_stand_by_id(id=id)
        return stand


async def get_all_stands(conn: AsyncSession):
    async with conn.begin():
        q = s.AsyncQuerier(await conn.connection())
        async for stand in q.get_all_stands():
            yield stand


async def update_stand(
    conn: AsyncSession, id: uuid.UUID, ent: UpdateStand
) -> m.Stand | None:
    async with conn.begin():
        q = s.AsyncQuerier(await conn.connection())
        stand = await q.update_stand(ent.to_params(id))
        return stand


async def delete_stand(conn: AsyncSession, id: uuid.UUID) -> bool:
    async with conn.begin():
        q = s.AsyncQuerier(await conn.connection())
        await q.delete_stand(id=id)
        return True