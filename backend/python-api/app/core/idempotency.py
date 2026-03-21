import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.responses import JSONResponse, Response
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.errors import ApiError, ErrorCode
from app.db.models import IdempotencyRecord


@dataclass(frozen=True)
class IdempotencyReplay:
    status_code: int
    response_body: dict[str, Any] | list[Any] | None

    def to_http_response(self) -> Response:
        if self.response_body is None:
            return Response(status_code=self.status_code)
        return JSONResponse(status_code=self.status_code, content=self.response_body)


@dataclass(frozen=True)
class IdempotencyContext:
    user_id: str
    request_method: str
    request_path: str
    idempotency_key: str
    payload_fingerprint: str
    existing_record_id: str | None


@dataclass(frozen=True)
class IdempotencyPrecheck:
    context: IdempotencyContext | None = None
    replay: IdempotencyReplay | None = None


def _normalize_idempotency_key(idempotency_key: str | None) -> str | None:
    if idempotency_key is None:
        return None

    normalized = idempotency_key.strip()
    if not normalized:
        return None

    if len(normalized) > 128:
        raise ApiError(
            code=ErrorCode.VALIDATION_ERROR,
            message="Idempotency-Key must be at most 128 characters",
            status_code=422,
            details={"header": "Idempotency-Key"},
        )

    return normalized


def _normalize_payload(payload_bytes: bytes | None) -> Any:
    if payload_bytes is None:
        return None

    stripped = payload_bytes.strip()
    if not stripped:
        return None

    try:
        return json.loads(stripped.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return stripped.decode("utf-8", errors="replace")


def _build_payload_fingerprint(request_method: str, request_path: str, payload: Any) -> str:
    canonical = json.dumps(
        {
            "request_method": request_method.upper(),
            "request_path": request_path,
            "payload": payload,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


async def _get_record_for_scope(
    db: AsyncSession,
    *,
    user_id: str,
    request_method: str,
    request_path: str,
    idempotency_key: str,
) -> IdempotencyRecord | None:
    stmt: Select[tuple[IdempotencyRecord]] = (
        select(IdempotencyRecord)
        .where(IdempotencyRecord.user_id == user_id)
        .where(IdempotencyRecord.request_method == request_method.upper())
        .where(IdempotencyRecord.request_path == request_path)
        .where(IdempotencyRecord.idempotency_key == idempotency_key)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


def _build_replay(record: IdempotencyRecord) -> IdempotencyReplay:
    body = record.response_body
    if isinstance(body, dict):
        return IdempotencyReplay(status_code=record.response_status_code, response_body=body)
    if isinstance(body, list):
        return IdempotencyReplay(status_code=record.response_status_code, response_body=body)
    return IdempotencyReplay(status_code=record.response_status_code, response_body=None)


async def prepare_mutation_idempotency(
    db: AsyncSession,
    *,
    user_id: str,
    request_method: str,
    request_path: str,
    idempotency_key: str | None,
    payload_bytes: bytes | None,
) -> IdempotencyPrecheck:
    normalized_key = _normalize_idempotency_key(idempotency_key)
    if normalized_key is None:
        return IdempotencyPrecheck()

    normalized_payload = _normalize_payload(payload_bytes)
    payload_fingerprint = _build_payload_fingerprint(request_method, request_path, normalized_payload)

    existing = await _get_record_for_scope(
        db,
        user_id=user_id,
        request_method=request_method,
        request_path=request_path,
        idempotency_key=normalized_key,
    )

    now = datetime.now(UTC)
    if existing is not None and existing.expires_at > now:
        if existing.payload_fingerprint != payload_fingerprint:
            raise ApiError(
                code=ErrorCode.IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD,
                message="This Idempotency-Key was already used with a different payload",
                status_code=409,
                details={
                    "request_method": request_method.upper(),
                    "request_path": request_path,
                },
            )
        return IdempotencyPrecheck(replay=_build_replay(existing))

    return IdempotencyPrecheck(
        context=IdempotencyContext(
            user_id=user_id,
            request_method=request_method.upper(),
            request_path=request_path,
            idempotency_key=normalized_key,
            payload_fingerprint=payload_fingerprint,
            existing_record_id=existing.id if existing is not None else None,
        )
    )


async def persist_mutation_idempotency(
    db: AsyncSession,
    *,
    context: IdempotencyContext | None,
    response_status_code: int,
    response_body: dict[str, Any] | list[Any] | None,
) -> IdempotencyReplay | None:
    if context is None:
        return None

    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.idempotency_replay_ttl_minutes)

    if context.existing_record_id is not None:
        existing = await db.get(IdempotencyRecord, context.existing_record_id)
        if existing is not None:
            existing.payload_fingerprint = context.payload_fingerprint
            existing.response_status_code = response_status_code
            existing.response_body = response_body
            existing.expires_at = expires_at
            await db.commit()
            return None

    try:
        record = IdempotencyRecord(
            user_id=context.user_id,
            request_method=context.request_method,
            request_path=context.request_path,
            idempotency_key=context.idempotency_key,
            payload_fingerprint=context.payload_fingerprint,
            response_status_code=response_status_code,
            response_body=response_body,
            expires_at=expires_at,
        )
        db.add(record)
        await db.commit()
    except IntegrityError as err:
        await db.rollback()
        existing = await _get_record_for_scope(
            db,
            user_id=context.user_id,
            request_method=context.request_method,
            request_path=context.request_path,
            idempotency_key=context.idempotency_key,
        )
        if existing is None:
            raise

        if existing.expires_at <= datetime.now(UTC):
            raise err

        if existing.payload_fingerprint != context.payload_fingerprint:
            raise ApiError(
                code=ErrorCode.IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD,
                message="This Idempotency-Key was already used with a different payload",
                status_code=409,
                details={
                    "request_method": context.request_method,
                    "request_path": context.request_path,
                },
            ) from err

        return _build_replay(existing)

    return None
