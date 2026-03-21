from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest

from app.core.errors import ApiError
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists import service


@pytest.mark.asyncio
async def test_reset_list_for_user_creates_snapshot_and_resets(monkeypatch: pytest.MonkeyPatch) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")

    class DummySession:
        @asynccontextmanager
        async def begin(self) -> AsyncIterator[None]:
            yield

    db = DummySession()

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    monkeypatch.setattr(service.repository, "list_items", AsyncMock(return_value=[]))
    monkeypatch.setattr(service.repository, "serialize_items_snapshot", lambda _items: [])
    monkeypatch.setattr(
        service.repository,
        "create_pre_reset_snapshot",
        AsyncMock(return_value=SimpleNamespace(id="snapshot-1")),
    )
    monkeypatch.setattr(service.repository, "reset_items_purchase_flags", AsyncMock(return_value=4))

    result = await service.reset_list_for_user(cast(Any, db), principal, "list-1")

    assert result.list_id == "list-1"
    assert result.snapshot_id == "snapshot-1"
    assert result.reset_items_count == 4


@pytest.mark.asyncio
async def test_restore_latest_for_user_without_snapshot_returns_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")

    class DummySession:
        @asynccontextmanager
        async def begin(self) -> AsyncIterator[None]:
            yield

    db = DummySession()

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    monkeypatch.setattr(service.repository, "get_latest_pre_reset_snapshot", AsyncMock(return_value=None))

    with pytest.raises(ApiError) as exc:
        await service.restore_latest_for_user(cast(Any, db), principal, "list-1")

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_restore_latest_for_user_replaces_items(monkeypatch: pytest.MonkeyPatch) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")

    class DummySession:
        @asynccontextmanager
        async def begin(self) -> AsyncIterator[None]:
            yield

    db = DummySession()
    snapshot = SimpleNamespace(
        id="snapshot-1",
        payload={
            "items": [
                {
                    "name": "Milk",
                    "quantity": "1.00",
                    "unit": "l",
                    "category": "dairy",
                    "note": None,
                    "is_purchased": False,
                    "is_template_item": False,
                    "sort_index": 0,
                }
            ]
        },
    )

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    monkeypatch.setattr(service.repository, "get_latest_pre_reset_snapshot", AsyncMock(return_value=snapshot))
    monkeypatch.setattr(service.repository, "replace_list_items_from_snapshot", AsyncMock(return_value=1))

    result = await service.restore_latest_for_user(cast(Any, db), principal, "list-1")

    assert result.list_id == "list-1"
    assert result.snapshot_id == "snapshot-1"
    assert result.restored_items_count == 1
