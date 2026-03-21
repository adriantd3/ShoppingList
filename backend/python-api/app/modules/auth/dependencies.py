from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Select, select

from app.api.dependencies import DbSession
from app.core.errors import ApiError, ErrorCode
from app.core.security import decode_access_token
from app.db.models import User
from app.modules.auth.schemas import UserPrincipal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
TokenDep = Annotated[str | None, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, db: DbSession) -> UserPrincipal:
    if token is None:
        raise ApiError(
            code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Missing bearer token",
            status_code=401,
        )

    payload = decode_access_token(token)
    stmt: Select[tuple[User]] = select(User).where(User.id == payload.sub)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise ApiError(
            code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Invalid or inactive user",
            status_code=401,
        )

    return UserPrincipal(user_id=user.id, email=user.email)
