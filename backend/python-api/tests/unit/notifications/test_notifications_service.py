from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest

from app.core.errors import ApiError, ErrorCode
from app.modules.auth.schemas import UserPrincipal
from app.modules.notifications import service
from app.modules.notifications.schemas import (
    DevicePushTokenRegisterRequest,
    NotificationPreferencesUpdateRequest,
)


@pytest.mark.asyncio
async def test_get_profile_for_user_returns_profile(
    monkeypatch: pytest.MonkeyPatch,
    transactional_session: Any,
    principal_user: UserPrincipal,
) -> None:
    monkeypatch.setattr(
        service.repository,
        "get_user_by_id",
        AsyncMock(
            return_value=SimpleNamespace(
                id="user-1",
                email="user@example.com",
                display_name="Adri",
                is_active=True,
            )
        ),
    )

    profile = await service.get_profile_for_user(db=cast(Any, transactional_session), principal=principal_user)

    assert profile.user_id == "user-1"
    assert profile.email == "user@example.com"
    assert profile.display_name == "Adri"
    assert profile.is_active is True


@pytest.mark.asyncio
async def test_get_profile_for_user_raises_when_user_missing(
    monkeypatch: pytest.MonkeyPatch,
    transactional_session: Any,
    principal_user: UserPrincipal,
) -> None:
    monkeypatch.setattr(service.repository, "get_user_by_id", AsyncMock(return_value=None))

    with pytest.raises(ApiError) as exc:
        await service.get_profile_for_user(db=cast(Any, transactional_session), principal=principal_user)

    assert exc.value.status_code == 401
    assert exc.value.code == ErrorCode.AUTH_TOKEN_INVALID


@pytest.mark.asyncio
async def test_get_notification_preferences_for_user_bootstraps_defaults_when_missing(
    monkeypatch: pytest.MonkeyPatch,
    transactional_session: Any,
    principal_user: UserPrincipal,
) -> None:
    monkeypatch.setattr(service.repository, "get_notification_preferences", AsyncMock(return_value=None))
    upsert_mock = AsyncMock(
        return_value=SimpleNamespace(
            list_change_push_enabled=True,
            updated_at=datetime.now(UTC),
        )
    )
    monkeypatch.setattr(service.repository, "upsert_notification_preferences", upsert_mock)

    result = await service.get_notification_preferences_for_user(
        db=cast(Any, transactional_session),
        principal=principal_user,
    )

    assert result.list_change_push_enabled is True
    upsert_mock.assert_awaited_once_with(
        cast(Any, transactional_session),
        user_id=principal_user.user_id,
        list_change_push_enabled=True,
    )


@pytest.mark.asyncio
async def test_update_notification_preferences_for_user_uses_payload_flag(
    monkeypatch: pytest.MonkeyPatch,
    transactional_session: Any,
    principal_user: UserPrincipal,
) -> None:
    upsert_mock = AsyncMock(
        return_value=SimpleNamespace(
            list_change_push_enabled=False,
            updated_at=datetime.now(UTC),
        )
    )
    monkeypatch.setattr(service.repository, "upsert_notification_preferences", upsert_mock)

    result = await service.update_notification_preferences_for_user(
        db=cast(Any, transactional_session),
        principal=principal_user,
        payload=NotificationPreferencesUpdateRequest(list_change_push_enabled=False),
    )

    assert result.list_change_push_enabled is False
    upsert_mock.assert_awaited_once_with(
        cast(Any, transactional_session),
        user_id=principal_user.user_id,
        list_change_push_enabled=False,
    )


@pytest.mark.asyncio
async def test_register_push_token_for_user_passes_platform_and_token(
    monkeypatch: pytest.MonkeyPatch,
    transactional_session: Any,
    principal_user: UserPrincipal,
) -> None:
    now = datetime.now(UTC)
    upsert_token_mock = AsyncMock(
        return_value=SimpleNamespace(
            id="token-1",
            user_id=principal_user.user_id,
            platform="android",
            push_token="x" * 32,
            last_seen_at=now,
            created_at=now,
        )
    )
    monkeypatch.setattr(service.repository, "upsert_device_push_token", upsert_token_mock)

    result = await service.register_push_token_for_user(
        db=cast(Any, transactional_session),
        principal=principal_user,
        payload=DevicePushTokenRegisterRequest(platform="android", push_token="x" * 32),
    )

    assert result.platform == "android"
    assert result.push_token == "x" * 32
    upsert_token_mock.assert_awaited_once_with(
        cast(Any, transactional_session),
        user_id=principal_user.user_id,
        platform="android",
        push_token="x" * 32,
    )
