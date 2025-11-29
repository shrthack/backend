import pydantic
import uuid


class UpsertPoints(pydantic.BaseModel):
    user_id: uuid.UUID
    points: int


class Point(pydantic.BaseModel):
    user_id: uuid.UUID
    total_points: int


class Error(pydantic.BaseModel):
    detail: str