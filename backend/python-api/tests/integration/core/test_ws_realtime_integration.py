from collections.abc import AsyncGenerator, Generator
from dataclasses import dataclass, field

import pytest
from fastapi import WebSocket
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.main import create_app


@dataclass
class FanoutOnSecondConnectManager:
    payload: dict[str, object]
    connections: dict[str, list[WebSocket]] = field(default_factory=dict)

    async def connect(self, list_id: str, websocket: WebSocket) -> None:
        listeners = self.connections.setdefault(list_id, [])
        listeners.append(websocket)
        if len(listeners) == 2:
            for conn in list(listeners):
                await conn.send_json(self.payload)

    async def disconnect(self, list_id: str, websocket: WebSocket) -> None:
        listeners = self.connections.get(list_id)
        if listeners is None:
            return
        if websocket in listeners:
            listeners.remove(websocket)
        if not listeners:
            self.connections.pop(list_id, None)


@dataclass
class OrderedEventsOnConnectManager:
    payloads: list[dict[str, object]]

    async def connect(self, _list_id: str, websocket: WebSocket) -> None:
        for payload in self.payloads:
            await websocket.send_json(payload)

    async def disconnect(self, _list_id: str, _websocket: WebSocket) -> None:
        return None


@dataclass
class NoopManager:
    async def connect(self, _list_id: str, _websocket: WebSocket) -> None:
        return None

    async def disconnect(self, _list_id: str, _websocket: WebSocket) -> None:
        return None


@pytest.fixture
def realtime_ws_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.db.session import get_db_session

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    app = create_app()
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_ws_fanout_sends_same_envelope_to_multiple_clients(
    realtime_ws_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.api.ws import router as ws_router

    envelope = {
        "event_id": "event-1",
        "event_type": "list.item.updated",
        "list_id": "list-1",
        "occurred_at": "2026-03-21T12:00:00Z",
        "actor_user_id": "user-1",
        "payload": {"item_id": "item-1", "is_purchased": True},
        "version": 1,
    }

    monkeypatch.setattr(ws_router, "connection_manager", FanoutOnSecondConnectManager(payload=envelope))
    monkeypatch.setattr(ws_router, "get_websocket_subject", lambda _ws: "user-1")

    async def fake_get_membership_role(*_args: object, **_kwargs: object) -> str:
        return "member"

    monkeypatch.setattr(ws_router, "get_membership_role", fake_get_membership_role)

    with realtime_ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy") as first:
        with realtime_ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy") as second:
            first_payload = first.receive_json()
            second_payload = second.receive_json()

    assert first_payload == envelope
    assert second_payload == envelope
    assert set(first_payload.keys()) == {
        "event_id",
        "event_type",
        "list_id",
        "occurred_at",
        "actor_user_id",
        "payload",
        "version",
    }


def test_ws_sequential_events_preserve_order(
    realtime_ws_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.api.ws import router as ws_router

    payloads = [
        {
            "event_id": "event-1",
            "event_type": "list.item.created",
            "list_id": "list-1",
            "occurred_at": "2026-03-21T12:00:00Z",
            "actor_user_id": "user-1",
            "payload": {"item_id": "item-1"},
            "version": 1,
        },
        {
            "event_id": "event-2",
            "event_type": "list.item.updated",
            "list_id": "list-1",
            "occurred_at": "2026-03-21T12:00:01Z",
            "actor_user_id": "user-1",
            "payload": {"item_id": "item-1", "is_purchased": True},
            "version": 1,
        },
    ]

    monkeypatch.setattr(ws_router, "connection_manager", OrderedEventsOnConnectManager(payloads=payloads))
    monkeypatch.setattr(ws_router, "get_websocket_subject", lambda _ws: "user-1")

    async def fake_get_membership_role(*_args: object, **_kwargs: object) -> str:
        return "member"

    monkeypatch.setattr(ws_router, "get_membership_role", fake_get_membership_role)

    with realtime_ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy") as websocket:
        first_event = websocket.receive_json()
        second_event = websocket.receive_json()

    assert first_event["event_type"] == "list.item.created"
    assert second_event["event_type"] == "list.item.updated"
    assert first_event["occurred_at"] < second_event["occurred_at"]


def test_ws_allows_join_transition_after_membership_change(
    realtime_ws_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.api.ws import router as ws_router

    role_checks = iter([None, "member"])

    monkeypatch.setattr(ws_router, "connection_manager", NoopManager())
    monkeypatch.setattr(ws_router, "get_websocket_subject", lambda _ws: "user-2")

    async def fake_get_membership_role(*_args: object, **_kwargs: object) -> str | None:
        return next(role_checks)

    monkeypatch.setattr(ws_router, "get_membership_role", fake_get_membership_role)

    with pytest.raises(WebSocketDisconnect) as rejected:
        with realtime_ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy"):
            pass

    assert rejected.value.code == 4403

    with realtime_ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy") as websocket:
        websocket.send_text("ping")
