import jwt
import uuid
import time


def generate(id: uuid.UUID, secret: str) -> str:
    now = int(time.time())
    payload = {
        "sub": str(id),
        "iss": "my-issuer",
        "aud": "my-api",
        "iat": now,
        "nbf": now,
        "exp": now + 60 * 60,
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def verify(token: str, secret: str) -> dict:
    decoded = jwt.decode(
        token,
        secret,
        algorithms=["HS256"],
        audience="my-api",
        issuer="my-issuer",
        options={"require": ["sub", "iss", "aud", "exp", "iat", "nbf"]},
    )
    return decoded
