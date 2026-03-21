from datetime import UTC, datetime
from typing import Literal

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ListMembership, ShareLink, ShoppingList


async def get_list_for_member(db: AsyncSession, *, list_id: str, user_id: str) -> ShoppingList | None:
    stmt: Select[tuple[ShoppingList]] = (
        select(ShoppingList)
        .join(ListMembership, ListMembership.list_id == ShoppingList.id)
        .where(ShoppingList.id == list_id)
        .where(ListMembership.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_share_link(
    db: AsyncSession,
    *,
    list_id: str,
    token_hash: str,
    expires_at: datetime,
    created_by_user_id: str,
) -> ShareLink:
    share_link = ShareLink(
        list_id=list_id,
        token_hash=token_hash,
        expires_at=expires_at,
        created_by_user_id=created_by_user_id,
    )
    db.add(share_link)
    await db.flush()
    await db.refresh(share_link)
    return share_link


async def get_share_link(db: AsyncSession, *, list_id: str, share_link_id: str) -> ShareLink | None:
    stmt: Select[tuple[ShareLink]] = (
        select(ShareLink)
        .where(ShareLink.id == share_link_id)
        .where(ShareLink.list_id == list_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_share_link_by_hash(db: AsyncSession, *, token_hash: str) -> ShareLink | None:
    stmt: Select[tuple[ShareLink]] = select(ShareLink).where(ShareLink.token_hash == token_hash)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def revoke_share_link(db: AsyncSession, *, share_link: ShareLink, actor_user_id: str) -> ShareLink:
    share_link.revoked_at = datetime.now(UTC)
    share_link.revoked_by_user_id = actor_user_id
    await db.flush()
    await db.refresh(share_link)
    return share_link


async def expire_share_link(db: AsyncSession, *, share_link: ShareLink) -> ShareLink:
    now = datetime.now(UTC)
    share_link.expires_at = now
    if share_link.revoked_at is None:
        share_link.revoked_at = now
    await db.flush()
    await db.refresh(share_link)
    return share_link


async def get_membership_role(db: AsyncSession, *, list_id: str, user_id: str) -> str | None:
    stmt: Select[tuple[ListMembership]] = (
        select(ListMembership)
        .where(ListMembership.list_id == list_id)
        .where(ListMembership.user_id == user_id)
    )
    result = await db.execute(stmt)
    membership = result.scalar_one_or_none()
    return membership.role if membership else None


async def upsert_member_role(
    db: AsyncSession,
    *,
    list_id: str,
    user_id: str,
    role: Literal["member", "owner"] = "member",
) -> str:
    stmt: Select[tuple[ListMembership]] = (
        select(ListMembership)
        .where(ListMembership.list_id == list_id)
        .where(ListMembership.user_id == user_id)
    )
    result = await db.execute(stmt)
    membership = result.scalar_one_or_none()

    if membership is not None:
        return membership.role

    membership = ListMembership(list_id=list_id, user_id=user_id, role=role)
    db.add(membership)
    await db.flush()
    return membership.role
