import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db import merch as c
from db import models as m
from ..entities.merch import CreateMerch, UpdateMerch


async def create(conn: AsyncSession, ent: CreateMerch) -> m.Merch | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        merch = await q.create_merch(**ent.to_params())
        return merch


async def get(conn: AsyncSession, id: uuid.UUID) -> m.Merch | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        merch = await q.get_merch_by_id(id=id)
        return merch


async def get_all(conn: AsyncSession) -> list[m.Merch]:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        merch_list = []
        async for merch in q.get_all_merch():
            merch_list.append(merch)
        return merch_list


async def update(
    conn: AsyncSession, id: uuid.UUID, ent: UpdateMerch
) -> m.Merch | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        merch = await q.update_merch(ent.to_params(id))
        return merch


async def delete(conn: AsyncSession, id: uuid.UUID) -> bool:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        await q.delete_merch(id=id)
        return True