from app.core.errors import ApiError, ErrorCode
from app.core.request_context import get_request_context
from app.modules.notifications import repository
from app.modules.notifications.schemas import (
    DevicePushTokenRegisterRequest,
    DevicePushTokenResponse,
    NotificationPreferencesResponse,
    NotificationPreferencesUpdateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)


async def get_profile_for_user() -> ProfileResponse:
    context = get_request_context()
    db = context.db
    principal = context.principal
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
    payload: ProfileUpdateRequest,
) -> ProfileResponse:
    context = get_request_context()
    db = context.db
    principal = context.principal
    user = await repository.get_user_by_id(db, user_id=principal.user_id)
    if user is None:
        raise ApiError(
            code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Invalid or inactive user",
            status_code=401,
        )

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
) -> NotificationPreferencesResponse:
    context = get_request_context()
    db = context.db
    principal = context.principal
    preferences = await repository.get_notification_preferences(db, user_id=principal.user_id)
    if preferences is None:
        preferences = await repository.upsert_notification_preferences(
            db,
            user_id=principal.user_id,
            list_change_push_enabled=True,
        )

    return NotificationPreferencesResponse.model_validate(preferences)


async def update_notification_preferences_for_user(
    payload: NotificationPreferencesUpdateRequest,
) -> NotificationPreferencesResponse:
    context = get_request_context()
    db = context.db
    principal = context.principal
    preferences = await repository.upsert_notification_preferences(
        db,
        user_id=principal.user_id,
        list_change_push_enabled=payload.list_change_push_enabled,
    )
    return NotificationPreferencesResponse.model_validate(preferences)


async def register_push_token_for_user(
    payload: DevicePushTokenRegisterRequest,
) -> DevicePushTokenResponse:
    context = get_request_context()
    db = context.db
    principal = context.principal
    token = await repository.upsert_device_push_token(
        db,
        user_id=principal.user_id,
        platform=payload.platform,
        push_token=payload.push_token,
    )
    return DevicePushTokenResponse.model_validate(token)
