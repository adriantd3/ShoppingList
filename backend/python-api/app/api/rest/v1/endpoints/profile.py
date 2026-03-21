from fastapi import APIRouter, status

from app.modules.auth.context import AuthenticatedContextDep
from app.modules.notifications.schemas import (
    DevicePushTokenRegisterRequest,
    DevicePushTokenResponse,
    NotificationPreferencesResponse,
    NotificationPreferencesUpdateRequest,
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.modules.notifications.service import (
    get_notification_preferences_for_user,
    get_profile_for_user,
    register_push_token_for_user,
    update_notification_preferences_for_user,
    update_profile_for_user,
)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileResponse)
async def get_profile(_: AuthenticatedContextDep) -> ProfileResponse:
    return await get_profile_for_user()


@router.patch("", response_model=ProfileResponse)
async def patch_profile(
    payload: ProfileUpdateRequest,
    _: AuthenticatedContextDep,
) -> ProfileResponse:
    return await update_profile_for_user(payload)


@router.get("/notifications", response_model=NotificationPreferencesResponse)
async def get_notification_preferences(
    _: AuthenticatedContextDep,
) -> NotificationPreferencesResponse:
    return await get_notification_preferences_for_user()


@router.patch("/notifications", response_model=NotificationPreferencesResponse)
async def patch_notification_preferences(
    payload: NotificationPreferencesUpdateRequest,
    _: AuthenticatedContextDep,
) -> NotificationPreferencesResponse:
    return await update_notification_preferences_for_user(payload)


@router.post("/push-tokens", response_model=DevicePushTokenResponse, status_code=status.HTTP_201_CREATED)
async def register_push_token(
    payload: DevicePushTokenRegisterRequest,
    _: AuthenticatedContextDep,
) -> DevicePushTokenResponse:
    return await register_push_token_for_user(payload)
