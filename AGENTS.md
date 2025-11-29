# Agent Instructions for Shorthack Backend

## Commands
- **Install**: `poetry install`
- **Run**: `poetry run python src/main.py`
- **Generate DB code**: `sqlc generate`
- **Docker run**: `docker-compose up`
- **Single test**: No test framework configured yet
- **Lint**: No linter configured yet
- **Format**: No formatter configured yet

## Code Style & Best Practices

### Imports
- **Order**: stdlib → third-party → local (alphabetical within groups)
- **Local imports**: Use relative imports (`..`) for internal modules
- **Typing imports**: `from typing import` first, then other stdlib

**Good:**
```python
from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..infra import jwt
from internal.deps import security
```

**Bad:**
```python
import uuid
from internal.deps import security
from fastapi import APIRouter
from typing import Annotated
from ..infra import jwt
```

### Naming Conventions
- **Functions/variables**: snake_case
- **Classes**: PascalCase
- **Constants**: UPPER_CASE
- **Methods**: snake_case, descriptive names like `to_params()`

### Types & Type Hints
- **Required**: Full type hints everywhere
- **Unions**: Use `|` instead of `Union` (Python 3.10+)
- **Optional**: Use `X | None` instead of `Optional[X]`
- **Annotated**: Use for FastAPI dependencies

**Good:**
```python
def signup(body: CreateClient, session: AsyncSession = Depends(db_session)) -> SignUpResp | None | Error:
    token: Annotated[dict, Depends(security.require_claims)]
```

**Bad:**
```python
def signup(body, session):
    # No type hints
```

### Async/Await
- **DB operations**: Always use async/await with AsyncSession
- **Transactions**: Use `async with conn.begin():` for transaction blocks
- **Connection**: Get querier with `q = c.AsyncQuerier(await conn.connection())`

**Good:**
```python
async def create(conn: AsyncSession, ent: CreateClient) -> m.Client | None:
    async with conn.begin():
        q = c.AsyncQuerier(await conn.connection())
        client = await q.create_client(ent.to_params())
        return client
```

### Error Handling
- **API errors**: HTTPException with status codes
- **DB errors**: try/except for IntegrityError/NoResultFound
- **Validation**: Use assert for critical checks
- **Return None**: For not found cases, return None and handle in handler

**Good:**
```python
try:
    dto = await client.create(session, body)
    assert dto is not None
    return SignUpResp(token=jwt.generate(dto.id, SECRET))
except IntegrityError:
    raise HTTPException(status_code=400, detail="Client already exists")
```

**Bad:**
```python
# Don't catch broad exceptions
try:
    # some code
except Exception:
    pass
```

### Models & Entities
- **Entities**: Pydantic BaseModel with full type hints
- **DB models**: Use SQLC-generated models
- **Conversion**: Add `to_params()` methods for entity → DB conversion

**Good:**
```python
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
```

### Auth & Security
- **Passwords**: Argon2 hashing, never store plain passwords
- **JWT**: HS256 algorithm, 1-hour expiration, include sub/iss/aud claims
- **Dependencies**: Use Annotated with Depends for auth requirements

### SQL & Database
- **Queries**: Use sqlc for type-safe queries
- **Migrations**: Use goose format with -- +goose Up
- **Parameters**: Use sqlc.arg() and sqlc.narg() for optional params
- **Coalesce**: Use coalesce() for optional updates

**Good:**
```sql
-- name: UpdateClient :one
update client
set
    name = coalesce(sqlc.narg('name'), name),
    surname = coalesce(sqlc.narg('surname'), surname),
    image_url = coalesce(sqlc.narg('image_url'), image_url)
where id = $1
returning *;
```

### Architecture Layers
- **Handlers**: FastAPI routes, HTTP concerns, error responses
- **Cases**: Business logic, transaction management
- **Entities**: Data models, validation, conversion methods
- **Infra**: External integrations (DB, JWT, hashing)

### Code Structure Patterns
- **Handler functions**: Take entities as input, return entities or raise HTTPException
- **Case functions**: Take AsyncSession and entities, return DB models or None
- **Entity methods**: Pure functions for conversion/validation
- **Infra functions**: Stateless utilities

**Always follow these patterns exactly - agents must mimic the existing codebase style precisely.**</content>
