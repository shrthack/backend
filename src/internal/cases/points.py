import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db import points as p
from db import models as m


async def upsert_points(conn: AsyncSession, user_id: uuid.UUID, points: int) -> m.Point | None:
    async with conn.begin():
        q = p.AsyncQuerier(await conn.connection())
        point = await q.upsert_points(user_id=user_id, total_points=points)
        return point


async def get_points(conn: AsyncSession, user_id: uuid.UUID) -> m.Point | None:
    async with conn.begin():
        q = p.AsyncQuerier(await conn.connection())
        point = await q.get_points_by_user_id(user_id=user_id)
        return point