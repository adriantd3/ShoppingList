import hashlib
import json
from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.core.errors import ApiError, ErrorCode
from app.core.idempotency import IdempotencyContext, IdempotencyPrecheck, IdempotencyReplay
from app.main import create_app
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.schemas import ListResponse


@pytest.fixture
def idempotency_lists_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.api.rest.v1.endpoints import lists as lists_endpoint
    from app.db.session import get_db_session

    replay_store: dict[str, tuple[str, int, dict[str, object] | None]] = {}
    service_calls = {"create_list": 0}

    async def fake_get_current_user() -> UserPrincipal:
        return UserPrincipal(user_id="user-1", email="user@example.com")

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    def _fingerprint(request_method: str, request_path: str, payload_bytes: bytes | None) -> str:
        normalized_payload: object | None = None
        if payload_bytes and payload_bytes.strip():
            normalized_payload = json.loads(payload_bytes.decode("utf-8"))
        canonical = json.dumps(
            {
                "request_method": request_method.upper(),
                "request_path": request_path,
                "payload": normalized_payload,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    async def fake_prepare_mutation_idempotency(
        _db: object,
        *,
        user_id: str,
        request_method: str,
        request_path: str,
        idempotency_key: str | None,
        payload_bytes: bytes | None,
    ) -> IdempotencyPrecheck:
        if idempotency_key is None:
            return IdempotencyPrecheck()

        scoped_key = f"{user_id}:{request_method.upper()}:{request_path}:{idempotency_key.strip()}"
        payload_fingerprint = _fingerprint(request_method, request_path, payload_bytes)

        if scoped_key in replay_store:
            stored_fingerprint, status_code, response_body = replay_store[scoped_key]
            if stored_fingerprint != payload_fingerprint:
                raise ApiError(
                    code=ErrorCode.IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD,
                    message="This Idempotency-Key was already used with a different payload",
                    status_code=409,
                )
            return IdempotencyPrecheck(replay=IdempotencyReplay(status_code=status_code, response_body=response_body))

        return IdempotencyPrecheck(
            context=IdempotencyContext(
                user_id=user_id,
                request_method=request_method.upper(),
                request_path=request_path,
                idempotency_key=idempotency_key.strip(),
                payload_fingerprint=payload_fingerprint,
                existing_record_id=None,
            )
        )

    async def fake_persist_mutation_idempotency(
        _db: object,
        *,
        context: IdempotencyContext | None,
        response_status_code: int,
        response_body: dict[str, object] | list[object] | None,
    ) -> IdempotencyReplay | None:
        if context is None:
            return None

        scoped_key = f"{context.user_id}:{context.request_method}:{context.request_path}:{context.idempotency_key}"
        if isinstance(response_body, dict):
            stored_body: dict[str, object] | None = response_body
        else:
            stored_body = None
        replay_store[scoped_key] = (context.payload_fingerprint, response_status_code, stored_body)
        return None

    async def fake_create_list_for_user(*_args: object, **_kwargs: object) -> ListResponse:
        service_calls["create_list"] += 1
        return ListResponse(
            id=f"list-{service_calls['create_list']}",
            name="Weekly",
            status="active",
            owner_user_id="user-1",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    monkeypatch.setattr(lists_endpoint, "prepare_mutation_idempotency", fake_prepare_mutation_idempotency)
    monkeypatch.setattr(lists_endpoint, "persist_mutation_idempotency", fake_persist_mutation_idempotency)
    monkeypatch.setattr(lists_endpoint, "create_list_for_user", fake_create_list_for_user)

    app = create_app()
    app.dependency_overrides[get_current_user] = fake_get_current_user
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_idempotency_replay_returns_same_create_list_response(idempotency_lists_client: TestClient) -> None:
    first = idempotency_lists_client.post(
        "/api/v1/lists",
        headers={"Idempotency-Key": "idem-create-1"},
        json={"name": "Weekly"},
    )
    second = idempotency_lists_client.post(
        "/api/v1/lists",
        headers={"Idempotency-Key": "idem-create-1"},
        json={"name": "Weekly"},
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json() == second.json()


def test_idempotency_reused_key_with_different_payload_returns_conflict(idempotency_lists_client: TestClient) -> None:
    first = idempotency_lists_client.post(
        "/api/v1/lists",
        headers={"Idempotency-Key": "idem-create-2"},
        json={"name": "Weekly"},
    )
    second = idempotency_lists_client.post(
        "/api/v1/lists",
        headers={"Idempotency-Key": "idem-create-2"},
        json={"name": "Other Name"},
    )

    assert first.status_code == 201
    assert second.status_code == 409
    payload = second.json()
    assert payload["error"]["code"] == "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD"


def test_create_list_without_idempotency_key_keeps_normal_behavior(idempotency_lists_client: TestClient) -> None:
    first = idempotency_lists_client.post("/api/v1/lists", json={"name": "Weekly"})
    second = idempotency_lists_client.post("/api/v1/lists", json={"name": "Weekly"})

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
