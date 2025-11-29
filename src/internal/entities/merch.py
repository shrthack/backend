import pydantic
import uuid

from db.merch import UpdateMerchParams


class Merch(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    info: str
    image_url: str
    points_needed: int


class CreateMerch(pydantic.BaseModel):
    name: str
    info: str
    image_url: str
    points_needed: int

    def to_params(self) -> dict:
        return {
            "name": self.name,
            "info": self.info,
            "image_url": self.image_url,
            "points_needed": self.points_needed,
        }


class UpdateMerch(pydantic.BaseModel):
    name: str | None
    info: str | None
    image_url: str | None
    points_needed: int | None

    def to_params(self, id: uuid.UUID) -> UpdateMerchParams:
        return UpdateMerchParams(
            id=id,
            name=self.name,
            info=self.info,
            image_url=self.image_url,
            points_needed=self.points_needed,
        )


class Error(pydantic.BaseModel):
    detail: str