import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..infra import jwt
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
        return SignUpResp(id=dto.id)
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
    return SignInResp(id=dto.id)


@router.get("/{id}", responses={404: {"model": Error}})
async def get_client(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Client | None:
    try:
        dto = await client.get(session, id)
        if dto is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return Client(
            id=dto.id,
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            image_url=dto.image_url,
            tg_username=dto.tg_username,
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Client not found")


@router.put("/{id}", responses={404: {"model": Error}})
async def update_client(
    id: uuid.UUID,
    ent: UpdateClient,
    session: AsyncSession = Depends(db_session),
) -> Client | None:
    dto = await client.update(session, id, ent)
    if dto is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return Client(
        id=dto.id,
        name=dto.name,
        surname=dto.surname,
        email=dto.email,
        image_url=dto.image_url,
        tg_username=dto.tg_username,
    )


@router.delete("/{id}", responses={204: {}, 404: {"model": Error}})
async def delete_client(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
) -> Response:
    if client.delete(session, id):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Client not found")
