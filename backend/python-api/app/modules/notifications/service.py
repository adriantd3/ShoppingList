from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApiError, ErrorCode
from app.modules.auth.schemas import UserPrincipal
from app.modules.notifications import repository
from app.modules.notifications.schemas import (
    DevicePushTokenRegisterRequest,
    DevicePushTokenResponse,
    NotificationPreferencesResponse,
    NotificationPreferencesUpdateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)


async def get_profile_for_user(*, db: AsyncSession, principal: UserPrincipal) -> ProfileResponse:
    user = await repository.get_user_by_id(db, user_id=principal.user_id)
    if user is None:
        raise ApiError(
            code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Invalid or inactive user",
            status_code=401,
        )

    return ProfileResponse(
        user_id=user.id,
        email=user.email,
        display_name=user.display_name,
        is_active=user.is_active,
    )


async def update_profile_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    payload: ProfileUpdateRequest,
) -> ProfileResponse:
    user = await repository.get_user_by_id(db, user_id=principal.user_id)
    if user is None:
        raise ApiError(
            code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Invalid or inactive user",
            status_code=401,
        )

    async with db.begin():
        updated = await repository.update_user_display_name(
            db,
            user=user,
            display_name=payload.display_name.strip(),
        )
    return ProfileResponse(
        user_id=updated.id,
        email=updated.email,
        display_name=updated.display_name,
        is_active=updated.is_active,
    )


async def get_notification_preferences_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
) -> NotificationPreferencesResponse:
    preferences = await repository.get_notification_preferences(db, user_id=principal.user_id)
    if preferences is None:
        async with db.begin():
            preferences = await repository.upsert_notification_preferences(
                db,
                user_id=principal.user_id,
                list_change_push_enabled=True,
            )

    return NotificationPreferencesResponse.model_validate(preferences)


async def update_notification_preferences_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    payload: NotificationPreferencesUpdateRequest,
) -> NotificationPreferencesResponse:
    async with db.begin():
        preferences = await repository.upsert_notification_preferences(
            db,
            user_id=principal.user_id,
            list_change_push_enabled=payload.list_change_push_enabled,
        )
    return NotificationPreferencesResponse.model_validate(preferences)


async def register_push_token_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    payload: DevicePushTokenRegisterRequest,
) -> DevicePushTokenResponse:
    async with db.begin():
        token = await repository.upsert_device_push_token(
            db,
            user_id=principal.user_id,
            platform=payload.platform,
            push_token=payload.push_token,
        )
    return DevicePushTokenResponse.model_validate(token)
