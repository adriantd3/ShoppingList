from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain_errors import AuthenticationServiceUnavailableError, InvalidCredentialsError
from app.core.security import create_access_token, verify_password
from app.modules.auth import repository
from app.modules.auth.schemas import LoginRequest, TokenResponse, UserPrincipal


async def authenticate_user(db: AsyncSession, payload: LoginRequest) -> UserPrincipal:
    try:
        row = await repository.get_user_with_password_identity(db, email=payload.email)
    except SQLAlchemyError as exc:
        raise AuthenticationServiceUnavailableError() from exc

    if not row:
        raise InvalidCredentialsError()

    user, identity = row
    if not user.is_active:
        raise InvalidCredentialsError()

    if not identity.password_hash or not verify_password(payload.password, identity.password_hash):
        raise InvalidCredentialsError()

    return UserPrincipal(user_id=user.id, email=user.email)


def issue_access_token(principal: UserPrincipal) -> TokenResponse:
    token = create_access_token(subject=principal.user_id)
    return TokenResponse(access_token=token)
