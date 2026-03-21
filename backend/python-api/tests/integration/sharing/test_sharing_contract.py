from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.core.errors import ApiError, ErrorCode
from app.main import create_app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.sharing.schemas import ShareLinkConsumeResponse, ShareLinkIssueResponse, ShareLinkResponse


@pytest.fixture
def sharing_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.api.rest.v1.endpoints import sharing as sharing_endpoint
    from app.db.session import get_db_session

    async def fake_get_current_user() -> UserPrincipal:
        return UserPrincipal(user_id="user-1", email="user@example.com")

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    async def fake_issue_share_link_for_user(*_args: object, **_kwargs: object) -> ShareLinkIssueResponse:
        return ShareLinkIssueResponse(
            link=ShareLinkResponse(
                id="link-1",
                list_id="list-1",
                expires_at=datetime.now(UTC) + timedelta(hours=24),
                revoked_at=None,
                revoked_by_user_id=None,
                created_by_user_id="user-1",
                created_at=datetime.now(UTC),
            ),
            token="issued-token-12345678901234567890",
        )

    async def fake_revoke_share_link_for_user(*_args: object, **_kwargs: object) -> ShareLinkResponse:
        return ShareLinkResponse(
            id="link-1",
            list_id="list-1",
            expires_at=datetime.now(UTC) + timedelta(hours=24),
            revoked_at=datetime.now(UTC),
            revoked_by_user_id="user-1",
            created_by_user_id="user-1",
            created_at=datetime.now(UTC),
        )

    async def fake_expire_share_link_for_user(*_args: object, **_kwargs: object) -> ShareLinkResponse:
        return ShareLinkResponse(
            id="link-1",
            list_id="list-1",
            expires_at=datetime.now(UTC),
            revoked_at=datetime.now(UTC),
            revoked_by_user_id="user-1",
            created_by_user_id="user-1",
            created_at=datetime.now(UTC),
        )

    async def fake_consume_share_link_for_user(*_args: object, **_kwargs: object) -> ShareLinkConsumeResponse:
        return ShareLinkConsumeResponse(list_id="list-1", membership_role="member")

    monkeypatch.setattr(sharing_endpoint, "issue_share_link_for_user", fake_issue_share_link_for_user)
    monkeypatch.setattr(sharing_endpoint, "revoke_share_link_for_user", fake_revoke_share_link_for_user)
    monkeypatch.setattr(sharing_endpoint, "expire_share_link_for_user", fake_expire_share_link_for_user)
    monkeypatch.setattr(sharing_endpoint, "consume_share_link_for_user", fake_consume_share_link_for_user)

    app = create_app()
    app.dependency_overrides[get_current_user] = fake_get_current_user
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_issue_share_link_contract(sharing_client: TestClient) -> None:
    response = sharing_client.post("/api/v1/lists/list-1/share-links", json={"expires_in_minutes": 120})

    assert response.status_code == 201
    payload = response.json()
    assert payload["token"]
    assert payload["link"]["list_id"] == "list-1"


def test_revoke_share_link_contract(sharing_client: TestClient) -> None:
    response = sharing_client.post("/api/v1/lists/list-1/share-links/link-1/revoke")

    assert response.status_code == 200
    payload = response.json()
    assert payload["revoked_by_user_id"] == "user-1"


def test_expire_share_link_contract(sharing_client: TestClient) -> None:
    response = sharing_client.post("/api/v1/lists/list-1/share-links/link-1/expire")

    assert response.status_code == 200
    payload = response.json()
    assert payload["revoked_at"] is not None


def test_consume_share_link_contract(sharing_client: TestClient) -> None:
    response = sharing_client.post("/api/v1/share-links/consume", json={"token": "issued-token-12345678901234567890"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["list_id"] == "list-1"
    assert payload["membership_role"] == "member"


def test_consume_share_link_expired_returns_contract(
    sharing_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.api.rest.v1.endpoints import sharing as sharing_endpoint

    async def fake_consume_share_link_expired(*_args: object, **_kwargs: object) -> ShareLinkConsumeResponse:
        raise ApiError(
            code=ErrorCode.SHARE_LINK_EXPIRED,
            message="Share link is expired",
            status_code=409,
        )

    monkeypatch.setattr(sharing_endpoint, "consume_share_link_for_user", fake_consume_share_link_expired)

    response = sharing_client.post("/api/v1/share-links/consume", json={"token": "expired-token-123456789012345678"})
    assert response.status_code == 409
    payload = response.json()
    assert payload["error"]["code"] == "SHARE_LINK_EXPIRED"
