from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..infra.jwt import verify
from internal.config import settings

security = HTTPBearer()
SECRET = settings.jwt_secret


def require_claims(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    token = creds.credentials
    try:
        decoded = verify(token, SECRET)
        if "sub" in decoded:
            return decoded
        else:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
