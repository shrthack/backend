from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..infra import jwt
from internal.deps import security
from ..infra.db import db_session
from ..cases import client
from ..entities.client import (
    Client,
    CreateClient,
    Error,
    SignInClient,
    SignInResp,
    SignUpResp,
    UpdateClient,
)
from internal.config import settings

router = APIRouter(prefix="/clients")
SECRET = settings.jwt_secret


@router.post("/sign-up", responses={400: {"model": Error}})
async def signup(
    body: CreateClient,
    session: AsyncSession = Depends(db_session),
) -> SignUpResp | None | Error:
    try:
        dto = await client.create(session, body)
        assert dto is not None
        return SignUpResp(token=jwt.generate(dto.id, SECRET))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Client already exists")


@router.post("/sign-in", responses={401: {"model": Error}})
async def signin(
    body: SignInClient,
    session: AsyncSession = Depends(db_session),
) -> SignInResp | None | Error:
    dto = await client.signin(session, body)
    if dto == None:
        raise HTTPException(status_code=401, detail="boo hoo")
    return SignInResp(token=jwt.generate(dto.id, SECRET))


@router.get("/{id}", responses={404: {"model": Error}})
async def get_client(
    token: Annotated[dict, Depends(security.require_claims)],
    session: AsyncSession = Depends(db_session),
) -> Client | None:
    try:
        dto = await client.get(session, uuid.UUID(token["sub"]))
        if dto is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return Client(
            id=dto.id,
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            image_url=dto.image_url,
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Client not found")


@router.put("/{id}", responses={404: {"model": Error}})
async def update_client(
    token: Annotated[dict, Depends(security.require_claims)],
    ent: UpdateClient,
    session: AsyncSession = Depends(db_session),
) -> Client | None:
    dto = await client.update(session, uuid.UUID(token["sub"]), ent)
    if dto is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return Client(
        id=dto.id,
        name=dto.name,
        surname=dto.surname,
        email=dto.email,
        image_url=dto.image_url,
    )


@router.delete("/", responses={204: {}, 404: {"model": Error}})
async def delete_client(
    token: Annotated[dict, Depends(security.require_claims)],
    session: AsyncSession = Depends(db_session),
) -> Response:
    if client.delete(session, uuid.UUID(token["sub"])):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Client not found")
