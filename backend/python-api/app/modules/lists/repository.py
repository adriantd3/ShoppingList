from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ListMembership


async def get_membership_role(db: AsyncSession, list_id: str, user_id: str) -> str | None:
    stmt: Select[tuple[ListMembership]] = (
        select(ListMembership)
        .where(ListMembership.list_id == list_id)
        .where(ListMembership.user_id == user_id)
    )
    result = await db.execute(stmt)
    membership = result.scalar_one_or_none()
    return membership.role if membership else None
