from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.schemas import ListResetResponse, ListRestoreLatestResponse


@pytest.fixture
def reset_restore_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.api.rest.v1.endpoints import lists as lists_endpoint
    from app.db.session import get_db_session

    async def fake_get_current_user() -> UserPrincipal:
        return UserPrincipal(user_id="user-1", email="user@example.com")

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    async def fake_reset_list_for_user(*_args: object, **_kwargs: object) -> ListResetResponse:
        return ListResetResponse(list_id="list-1", snapshot_id="snapshot-1", reset_items_count=5)

    async def fake_restore_latest_for_user(*_args: object, **_kwargs: object) -> ListRestoreLatestResponse:
        return ListRestoreLatestResponse(list_id="list-1", snapshot_id="snapshot-1", restored_items_count=5)

    monkeypatch.setattr(lists_endpoint, "reset_list_for_user", fake_reset_list_for_user)
    monkeypatch.setattr(lists_endpoint, "restore_latest_for_user", fake_restore_latest_for_user)

    app = create_app()
    app.dependency_overrides[get_current_user] = fake_get_current_user
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_reset_list_contract(reset_restore_client: TestClient) -> None:
    response = reset_restore_client.post("/api/v1/lists/list-1/reset")

    assert response.status_code == 200
    payload = response.json()
    assert payload["list_id"] == "list-1"
    assert payload["snapshot_id"] == "snapshot-1"
    assert payload["reset_items_count"] == 5


def test_restore_latest_contract(reset_restore_client: TestClient) -> None:
    response = reset_restore_client.post("/api/v1/lists/list-1/restore-latest")

    assert response.status_code == 200
    payload = response.json()
    assert payload["list_id"] == "list-1"
    assert payload["snapshot_id"] == "snapshot-1"
    assert payload["restored_items_count"] == 5
