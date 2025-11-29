from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def hash_password(plain_password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    ph = PasswordHasher()
    try:
        return ph.verify(password_hash, plain_password)
    except VerifyMismatchError:
        return False
