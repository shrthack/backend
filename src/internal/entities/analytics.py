from pydantic import BaseModel
import uuid
import datetime
import decimal


class CreateAnalytic(BaseModel):
    user_id: uuid.UUID
    stand_id: uuid.UUID


class Analytic(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    stand_id: uuid.UUID | None
    time: datetime.datetime


class AnalyticGrouped(BaseModel):
    date: datetime.date
    hour: decimal.Decimal
    count: int