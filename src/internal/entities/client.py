import pydantic
import uuid

from db.client import CreateClientParams, UpdateClientParams
from ..infra.hash import hash_password


class SignUpResp(pydantic.BaseModel):
    id: uuid.UUID


class SignInResp(pydantic.BaseModel):
    id: uuid.UUID


class CreateClient(pydantic.BaseModel):
    name: str
    surname: str
    email: str
    password: str
    image_url: str
    tg_username: str | None

    def to_params(self) -> CreateClientParams:
        return CreateClientParams(
            email=self.email,
            name=self.name,
            surname=self.surname,
            image_url=self.image_url,
            password_hash=hash_password(self.password),
            tg_username=self.tg_username,
        )


class SignInClient(pydantic.BaseModel):
    email: str
    password: str


class UpdateClient(pydantic.BaseModel):
    name: str | None
    surname: str | None
    image_url: str | None
    tg_username: str | None

    def to_params(self, id: uuid.UUID) -> UpdateClientParams:
        from db.client import UpdateClientParams
        return UpdateClientParams(
            id=id,
            name=self.name,
            surname=self.surname,
            image_url=self.image_url,
            tg_username=self.tg_username,
        )


class Client(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: str
    image_url: str
    tg_username: str | None


class Error(pydantic.BaseModel):
    detail: str
