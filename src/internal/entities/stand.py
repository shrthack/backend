import pydantic
import uuid

from db.stand import UpdateStandParams


class CreateStand(pydantic.BaseModel):
    name: str
    info: str
    location: str
    image_url: str

    def to_params(self):
        return {
            "name": self.name,
            "info": self.info,
            "location": self.location,
            "image_url": self.image_url,
        }


class UpdateStand(pydantic.BaseModel):
    name: str | None
    info: str | None
    location: str | None
    image_url: str | None

    def to_params(self, id: uuid.UUID) -> UpdateStandParams:
        return UpdateStandParams(
            id=id,
            name=self.name,
            info=self.info,
            location=self.location,
            image_url=self.image_url,
        )


class Stand(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    info: str
    location: str
    image_url: str


class Error(pydantic.BaseModel):
    detail: str