from datetime import UTC, datetime

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DevicePushToken, NotificationPreference, User


async def get_user_by_id(db: AsyncSession, *, user_id: str) -> User | None:
    stmt: Select[tuple[User]] = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_user_display_name(db: AsyncSession, *, user: User, display_name: str) -> User:
    user.display_name = display_name
    await db.commit()
    await db.refresh(user)
    return user


async def get_notification_preferences(db: AsyncSession, *, user_id: str) -> NotificationPreference | None:
    stmt: Select[tuple[NotificationPreference]] = select(NotificationPreference).where(NotificationPreference.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def upsert_notification_preferences(
    db: AsyncSession,
    *,
    user_id: str,
    list_change_push_enabled: bool,
) -> NotificationPreference:
    preferences = await get_notification_preferences(db, user_id=user_id)
    now = datetime.now(UTC)

    if preferences is None:
        preferences = NotificationPreference(
            user_id=user_id,
            list_change_push_enabled=list_change_push_enabled,
            updated_at=now,
        )
        db.add(preferences)
    else:
        preferences.list_change_push_enabled = list_change_push_enabled
        preferences.updated_at = now

    await db.commit()
    await db.refresh(preferences)
    return preferences


async def upsert_device_push_token(
    db: AsyncSession,
    *,
    user_id: str,
    platform: str,
    push_token: str,
) -> DevicePushToken:
    stmt: Select[tuple[DevicePushToken]] = (
        select(DevicePushToken)
        .where(DevicePushToken.user_id == user_id)
        .where(DevicePushToken.platform == platform)
        .where(DevicePushToken.push_token == push_token)
    )
    result = await db.execute(stmt)
    token = result.scalar_one_or_none()

    now = datetime.now(UTC)
    if token is None:
        token = DevicePushToken(
            user_id=user_id,
            platform=platform,
            push_token=push_token,
            last_seen_at=now,
        )
        db.add(token)
    else:
        token.last_seen_at = now

    await db.commit()
    await db.refresh(token)
    return token
