from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.main import create_app


@pytest.fixture
def ws_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.db.session import get_db_session

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    app = create_app()
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_ws_rejects_missing_token(ws_client: TestClient) -> None:
    with pytest.raises(WebSocketDisconnect) as exc:
        with ws_client.websocket_connect("/api/v1/ws/lists/list-1"):
            pass

    assert exc.value.code == 4401


def test_ws_rejects_non_member(ws_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.api.ws import router as ws_router

    monkeypatch.setattr(ws_router, "get_websocket_subject", lambda _ws: "user-1")

    async def fake_get_membership_role(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(ws_router, "get_membership_role", fake_get_membership_role)

    with pytest.raises(WebSocketDisconnect) as exc:
        with ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy"):
            pass

    assert exc.value.code == 4403


def test_ws_accepts_member(ws_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.api.ws import router as ws_router

    monkeypatch.setattr(ws_router, "get_websocket_subject", lambda _ws: "user-1")

    async def fake_get_membership_role(*_args: object, **_kwargs: object) -> str:
        return "member"

    monkeypatch.setattr(ws_router, "get_membership_role", fake_get_membership_role)

    with ws_client.websocket_connect("/api/v1/ws/lists/list-1?token=dummy") as websocket:
        websocket.send_text("ping")
