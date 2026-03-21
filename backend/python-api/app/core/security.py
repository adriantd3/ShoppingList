from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import uuid4

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.errors import ApiError, ErrorCode

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    jti: str


def hash_password(plain_password: str) -> str:
    return cast(str, pwd_context.hash(plain_password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    expire_delta = timedelta(minutes=expires_minutes or settings.jwt_access_token_expire_minutes)
    expire_at = now + expire_delta

    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire_at.timestamp()),
        "jti": str(uuid4()),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> TokenPayload:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "exp", "iat", "jti"]},
        )
        return TokenPayload(**payload)
    except jwt.InvalidTokenError as exc:
        raise ApiError(
            code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Invalid or expired token",
            status_code=401,
        ) from exc
