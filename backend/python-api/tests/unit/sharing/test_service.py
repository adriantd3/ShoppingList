import pytest

from app.core.request_context import clear_request_context, set_request_context
from app.modules.auth.context import AuthenticatedContext
from app.modules.sharing.service import hash_share_token


def test_hash_share_token_is_deterministic() -> None:
    token = "same-token-value"
    first = hash_share_token(token)
    second = hash_share_token(token)

    assert first == second
    assert len(first) == 64


def test_hash_share_token_does_not_return_plaintext() -> None:
    token = "plain-token"
    hashed = hash_share_token(token)

    assert hashed != token


@pytest.mark.asyncio
async def test_consume_share_link_emits_member_joined_for_new_member(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import UTC, datetime, timedelta
    from types import SimpleNamespace
    from unittest.mock import AsyncMock

    from app.modules.auth.schemas import UserPrincipal
    from app.modules.sharing import service
    from app.modules.sharing.schemas import ShareLinkConsumeRequest

    principal = UserPrincipal(user_id="user-1", email="user@example.com")
    db = AsyncMock()

    monkeypatch.setattr(
        service.repository,
        "get_share_link_by_hash",
        AsyncMock(
            return_value=SimpleNamespace(
                list_id="list-1",
                revoked_at=None,
                expires_at=datetime.now(UTC) + timedelta(minutes=10),
            )
        ),
    )
    monkeypatch.setattr(service.repository, "get_membership_role", AsyncMock(return_value=None))
    monkeypatch.setattr(service.repository, "upsert_member_role", AsyncMock(return_value="member"))
    emit_mock = AsyncMock()
    monkeypatch.setattr(service, "emit_list_event", emit_mock)

    context = AuthenticatedContext(db=db, principal=principal)
    token = set_request_context(context)
    try:
        result = await service.consume_share_link_for_user(payload=ShareLinkConsumeRequest(token="token-value-at-least-20"))
    finally:
        clear_request_context(token)

    assert result.list_id == "list-1"
    assert result.membership_role == "member"
    assert emit_mock.await_count == 1
    assert emit_mock.await_args is not None
    assert emit_mock.await_args.kwargs["event_type"] == "list.member.joined"
