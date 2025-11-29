import pydantic
import uuid

from db.event import UpdateEventParams


class CreateEvent(pydantic.BaseModel):
    name: str
    info: str
    image_url: str
    points: int

    def to_params(self):
        return {
            "name": self.name,
            "info": self.info,
            "image_url": self.image_url,
            "points": self.points,
        }


class UpdateEvent(pydantic.BaseModel):
    name: str | None
    info: str | None
    image_url: str | None
    points: int | None

    def to_params(self, id: uuid.UUID) -> UpdateEventParams:
        return UpdateEventParams(
            id=id,
            name=self.name,
            info=self.info,
            image_url=self.image_url,
            points=self.points,
        )


class Event(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    info: str
    image_url: str
    points: int


class CreateActiveEvent(pydantic.BaseModel):
    user_id: uuid.UUID
    event_id: uuid.UUID
    total_points: int

    def to_params(self):
        return {
            "user_id": self.user_id,
            "event_id": self.event_id,
            "total_points": self.total_points,
        }


class UpdateActiveEvent(pydantic.BaseModel):
    total_points: int | None

    def to_params(self, user_id: uuid.UUID):
        return {
            "user_id": user_id,
            "total_points": self.total_points,
        }


class ActiveEvent(pydantic.BaseModel):
    user_id: uuid.UUID
    event_id: uuid.UUID
    total_points: int


class Error(pydantic.BaseModel):
    detail: str