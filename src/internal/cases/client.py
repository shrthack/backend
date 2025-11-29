import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db import client as c
from db import models as m
from ..entities.client import CreateClient, SignInClient, UpdateClient
from ..infra import hash


async def create(conn: AsyncSession, ent: CreateClient) -> m.Client | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        client = await q.create_client(ent.to_params())
        return client


async def signin(conn: AsyncSession, ent: SignInClient) -> m.Client | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        client = await q.get_client_by_email(email=ent.email)
        if client == None:
            return None
        if hash.verify_password(ent.password, client.password_hash):
            return client


async def get(conn: AsyncSession, id: uuid.UUID) -> m.Client | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        client = await q.get_client_by_id(id=id)
        return client


async def update(
    conn: AsyncSession, id: uuid.UUID, ent: UpdateClient
) -> m.Client | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        client = await q.update_client(ent.to_params(id))
        return client


async def delete(conn: AsyncSession, id: uuid.UUID) -> bool:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        return await q.delete_client(id=id) is not None
