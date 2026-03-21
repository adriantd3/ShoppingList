from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.notifications.schemas import (
    DevicePushTokenResponse,
    NotificationPreferencesResponse,
    ProfileResponse,
)


@pytest.fixture
def profile_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.api.rest.v1.endpoints import profile as profile_endpoint
    from app.db.session import get_db_session

    async def fake_get_current_user() -> UserPrincipal:
        return UserPrincipal(user_id="user-1", email="user@example.com")

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    async def fake_get_profile_for_user(*_args: object, **_kwargs: object) -> ProfileResponse:
        return ProfileResponse(user_id="user-1", email="user@example.com", display_name="Adri", is_active=True)

    async def fake_update_profile_for_user(*_args: object, **_kwargs: object) -> ProfileResponse:
        return ProfileResponse(user_id="user-1", email="user@example.com", display_name="Updated", is_active=True)

    async def fake_get_notification_preferences_for_user(*_args: object, **_kwargs: object) -> NotificationPreferencesResponse:
        return NotificationPreferencesResponse(list_change_push_enabled=True, updated_at=datetime.now(UTC))

    async def fake_update_notification_preferences_for_user(*_args: object, **_kwargs: object) -> NotificationPreferencesResponse:
        return NotificationPreferencesResponse(list_change_push_enabled=False, updated_at=datetime.now(UTC))

    async def fake_register_push_token_for_user(*_args: object, **_kwargs: object) -> DevicePushTokenResponse:
        now = datetime.now(UTC)
        return DevicePushTokenResponse(
            id="token-1",
            user_id="user-1",
            platform="android",
            push_token="x" * 32,
            last_seen_at=now,
            created_at=now,
        )

    monkeypatch.setattr(profile_endpoint, "get_profile_for_user", fake_get_profile_for_user)
    monkeypatch.setattr(profile_endpoint, "update_profile_for_user", fake_update_profile_for_user)
    monkeypatch.setattr(
        profile_endpoint,
        "get_notification_preferences_for_user",
        fake_get_notification_preferences_for_user,
    )
    monkeypatch.setattr(
        profile_endpoint,
        "update_notification_preferences_for_user",
        fake_update_notification_preferences_for_user,
    )
    monkeypatch.setattr(profile_endpoint, "register_push_token_for_user", fake_register_push_token_for_user)

    app = create_app()
    app.dependency_overrides[get_current_user] = fake_get_current_user
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_get_profile_contract(profile_client: TestClient) -> None:
    response = profile_client.get("/api/v1/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["user_id"] == "user-1"
    assert payload["email"] == "user@example.com"


def test_patch_profile_contract(profile_client: TestClient) -> None:
    response = profile_client.patch("/api/v1/profile", json={"display_name": "Updated"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["display_name"] == "Updated"


def test_get_notification_preferences_contract(profile_client: TestClient) -> None:
    response = profile_client.get("/api/v1/profile/notifications")

    assert response.status_code == 200
    payload = response.json()
    assert payload["list_change_push_enabled"] is True


def test_patch_notification_preferences_contract(profile_client: TestClient) -> None:
    response = profile_client.patch("/api/v1/profile/notifications", json={"list_change_push_enabled": False})

    assert response.status_code == 200
    payload = response.json()
    assert payload["list_change_push_enabled"] is False


def test_register_push_token_contract(profile_client: TestClient) -> None:
    response = profile_client.post(
        "/api/v1/profile/push-tokens",
        json={"platform": "android", "push_token": "x" * 32},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] == "token-1"
    assert payload["platform"] == "android"
