from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApiError, ErrorCode
from app.core.security import create_access_token, verify_password
from app.db.models import AuthIdentity, User
from app.modules.auth.schemas import LoginRequest, TokenResponse, UserPrincipal


async def authenticate_user(db: AsyncSession, payload: LoginRequest) -> UserPrincipal:
    stmt: Select[tuple[User, AuthIdentity]] = (
        select(User, AuthIdentity)
        .join(AuthIdentity, AuthIdentity.user_id == User.id)
        .where(User.email == payload.email)
        .where(AuthIdentity.provider == "password")
    )
    result = await db.execute(stmt)
    row = result.first()

    if not row:
        raise ApiError(
            code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Invalid credentials",
            status_code=401,
        )

    user, identity = row
    if not user.is_active:
        raise ApiError(
            code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Invalid credentials",
            status_code=401,
        )

    if not identity.password_hash or not verify_password(payload.password, identity.password_hash):
        raise ApiError(
            code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Invalid credentials",
            status_code=401,
        )

    return UserPrincipal(user_id=user.id, email=user.email)


def issue_access_token(principal: UserPrincipal) -> TokenResponse:
    token = create_access_token(subject=principal.user_id)
    return TokenResponse(access_token=token)
