from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.dependencies import DbSession
from app.core.domain_errors import InvalidTokenError
from app.core.security import decode_access_token
from app.modules.auth import repository
from app.modules.auth.schemas import UserPrincipal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
TokenDep = Annotated[str | None, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, db: DbSession) -> UserPrincipal:
    if token is None:
        raise InvalidTokenError()

    payload = decode_access_token(token)
    user = await repository.get_user_by_id(db, user_id=payload.sub)

    if user is None or not user.is_active:
        raise InvalidTokenError()

    return UserPrincipal(user_id=user.id, email=user.email)
