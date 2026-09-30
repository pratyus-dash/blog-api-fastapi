import os

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from pwdlib import PasswordHash


load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret-key"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)


password_hash = PasswordHash.recommended()


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


def get_password_hash(
    password: str
) -> str:

    return password_hash.hash(
        password
    )


def create_access_token(
    data: dict
):

    to_encode = data.copy()


    expire = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


    to_encode.update({
        "exp": expire
    })


    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )