from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.modules.realtime import service


@pytest.mark.asyncio
async def test_emit_list_event_persists_notifies_and_broadcasts(monkeypatch: pytest.MonkeyPatch) -> None:
    created_event = SimpleNamespace(
        id="event-1",
        event_type="list.item.created",
        list_id="list-1",
        created_at=datetime.now(UTC),
        payload={"item_id": "item-1"},
    )

    create_mock = AsyncMock(return_value=created_event)
    notify_mock = AsyncMock()
    broadcast_mock = AsyncMock()

    monkeypatch.setattr(service, "create_realtime_event", create_mock)
    monkeypatch.setattr(service, "publish_notify", notify_mock)
    monkeypatch.setattr(service.connection_manager, "broadcast_event", broadcast_mock)

    envelope = await service.emit_list_event(
        AsyncMock(),
        list_id="list-1",
        actor_user_id="user-1",
        event_type="list.item.created",
        payload={"item_id": "item-1"},
    )

    assert envelope.event_id == "event-1"
    assert envelope.actor_user_id == "user-1"
    assert envelope.version == 1

    create_mock.assert_awaited_once()
    notify_mock.assert_awaited_once()
    broadcast_mock.assert_awaited_once()
