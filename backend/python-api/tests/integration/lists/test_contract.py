from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.schemas import ListItemResponse, ListResponse


@pytest.fixture
def lists_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.api.rest.v1.endpoints import lists as lists_endpoint
    from app.db.session import get_db_session

    async def fake_get_current_user() -> UserPrincipal:
        return UserPrincipal(user_id="user-1", email="user@example.com")

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    async def fake_create_list_for_user(*_args: object, **_kwargs: object) -> ListResponse:
        return ListResponse(
            id="list-1",
            name="Weekly",
            status="active",
            owner_user_id="user-1",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    async def fake_create_item_for_user(*_args: object, **_kwargs: object) -> ListItemResponse:
        return ListItemResponse(
            id="item-1",
            list_id="list-1",
            name="Milk",
            quantity=Decimal("1.00"),
            unit="l",
            category="dairy",
            note=None,
            is_purchased=False,
            is_template_item=False,
            sort_index=0,
            updated_at=datetime.now(UTC),
            updated_by_user_id="user-1",
        )

    monkeypatch.setattr(lists_endpoint, "create_list_for_user", fake_create_list_for_user)
    monkeypatch.setattr(lists_endpoint, "create_item_for_user", fake_create_item_for_user)

    app = create_app()
    app.dependency_overrides[get_current_user] = fake_get_current_user
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_create_list_contract(lists_client: TestClient) -> None:
    response = lists_client.post("/api/v1/lists", json={"name": "Weekly"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] == "list-1"
    assert payload["name"] == "Weekly"


def test_create_item_invalid_category_returns_validation_error(lists_client: TestClient) -> None:
    response = lists_client.post(
        "/api/v1/lists/list-1/items",
        json={
            "name": "Milk",
            "quantity": "1.00",
            "unit": "l",
            "category": "invalid-category",
            "is_purchased": False,
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_update_item_rejects_is_template_item_field(lists_client: TestClient) -> None:
    response = lists_client.patch(
        "/api/v1/lists/list-1/items/item-1",
        json={
            "is_template_item": True,
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "VALIDATION_ERROR"
