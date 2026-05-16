
import os
import jwt
from typing import Any
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone


load_dotenv()


jwt_secret = os.getenv("jwt_secret")
password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher()
    )
)

ALGORITHM = "HS256"

def verify_access_token(jwt_token: str):
    decoded_jwt = jwt.decode(jwt_token, jwt_secret , algorithm=ALGORITHM)

    return decoded_jwt.sub if decoded_jwt else None

def create_access_token(subject: str | Any , expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt

def get_hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(
        plain_password : str, hashed_password: str
) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password , hashed_password)

