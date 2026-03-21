from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AuthIdentity, User


async def get_user_with_password_identity(
    db: AsyncSession,
    *,
    email: str,
) -> tuple[User, AuthIdentity] | None:
    stmt: Select[tuple[User, AuthIdentity]] = (
        select(User, AuthIdentity)
        .join(AuthIdentity, AuthIdentity.user_id == User.id)
        .where(User.email == email)
        .where(AuthIdentity.provider == "password")
    )
    result = await db.execute(stmt)
    row = result.first()
    if row is None:
        return None
    return row[0], row[1]


async def get_user_by_id(
    db: AsyncSession,
    *,
    user_id: str,
) -> User | None:
    stmt: Select[tuple[User]] = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()