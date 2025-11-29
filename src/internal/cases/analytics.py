from sqlalchemy.ext.asyncio import AsyncSession

from internal.entities.analytics import CreateAnalytic, AnalyticGrouped
from db import analytics as a, models as m


async def create(conn: AsyncSession, ent: CreateAnalytic) -> m.Analytic | None:
    async with conn.begin():
        q = a.AsyncQuerier(await conn.connection())
        return await q.create_analytics(user_id=ent.user_id, stand_id=ent.stand_id)


async def get_grouped(conn: AsyncSession) -> list[AnalyticGrouped]:
    async with conn.begin():
        q = a.AsyncQuerier(await conn.connection())
        rows = []
        async for row in q.get_analytics_grouped():
            rows.append(AnalyticGrouped(date=row.date, hour=row.hour, count=row.count))
        return rows

