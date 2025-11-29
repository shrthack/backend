import pydantic
import uuid

from db.client import CreateClientParams
from ..infra.hash import hash_password


class SignUpResp(pydantic.BaseModel):
    token: str


class SignInResp(pydantic.BaseModel):
    token: str


class CreateClient(pydantic.BaseModel):
    name: str
    surname: str
    email: str
    password: str
    image_url: str

    def to_params(self) -> CreateClientParams:
        return CreateClientParams(
            email=self.email,
            name=self.name,
            surname=self.surname,
            image_url=self.image_url,
            password_hash=hash_password(self.password),
        )


class SignInClient(pydantic.BaseModel):
    email: str
    password: str


class UpdateClient(pydantic.BaseModel):
    name: str | None
    surname: str | None
    image_url: str | None


class Client(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: str
    image_url: str


class Error(pydantic.BaseModel):
    detail: str
