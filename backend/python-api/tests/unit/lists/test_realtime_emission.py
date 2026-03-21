from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest

from app.core.request_context import clear_request_context, set_request_context
from app.modules.auth.context import AuthenticatedContext
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists import schemas, service


def _item_fixture(*, is_purchased: bool) -> SimpleNamespace:
    return SimpleNamespace(
        id="item-1",
        list_id="list-1",
        name="Milk",
        quantity=Decimal("1.00"),
        unit="l",
        category="dairy",
        note=None,
        is_purchased=is_purchased,
        is_template_item=False,
        sort_index=0,
        updated_at=datetime.now(UTC),
        updated_by_user_id="user-1",
    )


@pytest.mark.asyncio
async def test_create_item_emits_created_event(monkeypatch: pytest.MonkeyPatch) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")
    db = AsyncMock()

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    created_item = _item_fixture(is_purchased=False)
    monkeypatch.setattr(service.repository, "get_next_sort_index", AsyncMock(return_value=0))
    monkeypatch.setattr(service.repository, "create_item", AsyncMock(return_value=created_item))
    emit_mock = AsyncMock()
    monkeypatch.setattr(service, "emit_list_event", emit_mock)

    payload = schemas.ListItemCreateRequest(
        name="Milk",
        quantity=Decimal("1.00"),
        unit="l",
        category="dairy",
        note=None,
        is_purchased=False,
    )
    context = AuthenticatedContext(db=db, principal=principal)
    token = set_request_context(context)
    try:
        await service.create_item_for_user("list-1", payload)
    finally:
        clear_request_context(token)

    assert emit_mock.await_count == 1
    assert emit_mock.await_args is not None
    assert emit_mock.await_args.kwargs["event_type"] == "list.item.created"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("old_state", "new_state", "expected_event"),
    [
        (False, True, "list.item.purchased_toggled"),
        (False, False, "list.item.updated"),
    ],
)
async def test_update_item_emits_expected_event(
    monkeypatch: pytest.MonkeyPatch,
    old_state: bool,
    new_state: bool,
    expected_event: str,
) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")
    db = AsyncMock()

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    monkeypatch.setattr(
        service.repository,
        "get_item_for_list",
        AsyncMock(return_value=_item_fixture(is_purchased=old_state)),
    )
    monkeypatch.setattr(
        service.repository,
        "update_item",
        AsyncMock(return_value=_item_fixture(is_purchased=new_state)),
    )
    emit_mock = AsyncMock()
    monkeypatch.setattr(service, "emit_list_event", emit_mock)

    payload = schemas.ListItemUpdateRequest(is_purchased=new_state)
    context = AuthenticatedContext(db=db, principal=principal)
    token = set_request_context(context)
    try:
        await service.update_item_for_user("list-1", "item-1", payload)
    finally:
        clear_request_context(token)

    assert emit_mock.await_count == 1
    assert emit_mock.await_args is not None
    assert emit_mock.await_args.kwargs["event_type"] == expected_event


@pytest.mark.asyncio
async def test_delete_item_emits_deleted_event(monkeypatch: pytest.MonkeyPatch) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")
    db = AsyncMock()

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    monkeypatch.setattr(service.repository, "get_item_for_list", AsyncMock(return_value=_item_fixture(is_purchased=False)))
    monkeypatch.setattr(service.repository, "delete_item", AsyncMock())
    emit_mock = AsyncMock()
    monkeypatch.setattr(service, "emit_list_event", emit_mock)

    context = AuthenticatedContext(db=db, principal=principal)
    token = set_request_context(context)
    try:
        await service.delete_item_for_user("list-1", "item-1")
    finally:
        clear_request_context(token)

    assert emit_mock.await_count == 1
    assert emit_mock.await_args is not None
    assert emit_mock.await_args.kwargs["event_type"] == "list.item.deleted"


@pytest.mark.asyncio
async def test_reset_and_restore_emit_events(monkeypatch: pytest.MonkeyPatch) -> None:
    principal = UserPrincipal(user_id="user-1", email="user@example.com")

    class DummySession:
        @asynccontextmanager
        async def begin(self) -> AsyncIterator[None]:
            yield

    db = DummySession()

    monkeypatch.setattr(service.repository, "get_list_for_member", AsyncMock(return_value=SimpleNamespace(id="list-1")))
    monkeypatch.setattr(service.repository, "list_items", AsyncMock(return_value=[]))
    monkeypatch.setattr(service.repository, "serialize_items_snapshot", lambda _items: [])
    monkeypatch.setattr(service.repository, "create_pre_reset_snapshot", AsyncMock(return_value=SimpleNamespace(id="snapshot-1")))
    monkeypatch.setattr(service.repository, "reset_items_purchase_flags", AsyncMock(return_value=2))
    monkeypatch.setattr(
        service.repository,
        "get_latest_pre_reset_snapshot",
        AsyncMock(return_value=SimpleNamespace(id="snapshot-2", payload={"items": []})),
    )
    monkeypatch.setattr(service.repository, "replace_list_items_from_snapshot", AsyncMock(return_value=2))
    emit_mock = AsyncMock()
    monkeypatch.setattr(service, "emit_list_event", emit_mock)

    context = AuthenticatedContext(db=cast(Any, db), principal=principal)
    token = set_request_context(context)
    try:
        await service.reset_list_for_user("list-1")
        await service.restore_latest_for_user("list-1")
    finally:
        clear_request_context(token)

    emitted_types = [call.kwargs["event_type"] for call in emit_mock.await_args_list]
    assert emitted_types == ["list.reset.performed", "list.restore.performed"]
