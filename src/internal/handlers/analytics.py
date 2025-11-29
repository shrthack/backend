from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from internal.entities.analytics import CreateAnalytic, Analytic, AnalyticGrouped
from internal.cases import analytics as c
from internal.infra.db import db_session

router = APIRouter()


@router.post("/analytics", response_model=Analytic)
async def create_analytic(
    body: CreateAnalytic,
    session: AsyncSession = Depends(db_session),
) -> Analytic:
    dto = await c.create(session, body)
    if dto is None:
        raise HTTPException(status_code=400, detail="Failed to create analytic")
    return Analytic(
        id=dto.id, user_id=dto.user_id, stand_id=dto.stand_id, time=dto.time
    )


@router.get("/analytics/grouped", response_model=list[AnalyticGrouped])
async def get_analytics_grouped(
    session: AsyncSession = Depends(db_session),
) -> list[AnalyticGrouped]:
    return await c.get_grouped(session)

