from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.errors import ApiError
from app.core.idempotency import (
    IdempotencyContext,
    _build_payload_fingerprint,
    _normalize_payload,
    persist_mutation_idempotency,
    prepare_mutation_idempotency,
)


@pytest.mark.asyncio
async def test_prepare_mutation_idempotency_skips_when_key_missing() -> None:
    db = AsyncMock()

    precheck = await prepare_mutation_idempotency(
        db,
        user_id="user-1",
        request_method="POST",
        request_path="/api/v1/lists",
        idempotency_key=None,
        payload_bytes=b'{"name":"Weekly"}',
    )

    assert precheck.context is None
    assert precheck.replay is None
    db.execute.assert_not_called()


@pytest.mark.asyncio
async def test_prepare_mutation_idempotency_replays_when_payload_matches() -> None:
    payload_bytes = b'{"name":"Weekly"}'
    expected_fingerprint = _build_payload_fingerprint("POST", "/api/v1/lists", _normalize_payload(payload_bytes))

    existing = SimpleNamespace(
        id="idem-1",
        payload_fingerprint=expected_fingerprint,
        response_status_code=201,
        response_body={"id": "list-1"},
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )
    query_result = MagicMock()
    query_result.scalar_one_or_none.return_value = existing

    db = AsyncMock()
    db.execute.return_value = query_result

    precheck = await prepare_mutation_idempotency(
        db,
        user_id="user-1",
        request_method="POST",
        request_path="/api/v1/lists",
        idempotency_key="key-1",
        payload_bytes=b'{"name":"Weekly"}',
    )

    assert precheck.context is None
    assert precheck.replay is not None
    assert precheck.replay.status_code == 201
    assert precheck.replay.response_body == {"id": "list-1"}


@pytest.mark.asyncio
async def test_prepare_mutation_idempotency_rejects_conflicting_payload() -> None:
    payload_bytes = b'{"name":"Weekly"}'

    existing = SimpleNamespace(
        id="idem-1",
        payload_fingerprint="different",
        response_status_code=201,
        response_body={"id": "list-1"},
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )
    query_result = MagicMock()
    query_result.scalar_one_or_none.return_value = existing

    db = AsyncMock()
    db.execute.return_value = query_result

    with pytest.raises(ApiError) as exc:
        await prepare_mutation_idempotency(
            db,
            user_id="user-1",
            request_method="POST",
            request_path="/api/v1/lists",
            idempotency_key="key-1",
            payload_bytes=payload_bytes,
        )

    assert exc.value.status_code == 409
    assert exc.value.code == "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD"


@pytest.mark.asyncio
async def test_persist_mutation_idempotency_creates_record() -> None:
    db = MagicMock()
    db.commit = AsyncMock()
    context = IdempotencyContext(
        user_id="user-1",
        request_method="POST",
        request_path="/api/v1/lists",
        idempotency_key="key-1",
        payload_fingerprint="fingerprint-1",
        existing_record_id=None,
    )

    replay = await persist_mutation_idempotency(
        db,
        context=context,
        response_status_code=201,
        response_body={"id": "list-1"},
    )

    assert replay is None
    db.add.assert_called_once()
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_persist_mutation_idempotency_updates_expired_record_slot() -> None:
    existing = SimpleNamespace(
        payload_fingerprint="old",
        response_status_code=200,
        response_body={"id": "list-0"},
        expires_at=datetime.now(UTC),
    )
    db = MagicMock()
    db.commit = AsyncMock()
    db.get = AsyncMock()
    db.get.return_value = existing

    context = IdempotencyContext(
        user_id="user-1",
        request_method="PATCH",
        request_path="/api/v1/lists/list-1",
        idempotency_key="key-1",
        payload_fingerprint="fingerprint-new",
        existing_record_id="idem-1",
    )

    replay = await persist_mutation_idempotency(
        db,
        context=context,
        response_status_code=200,
        response_body={"id": "list-1"},
    )

    assert replay is None
    assert existing.payload_fingerprint == "fingerprint-new"
    assert existing.response_status_code == 200
    assert existing.response_body == {"id": "list-1"}
    db.commit.assert_awaited_once()
