from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient

from app.core.domain_errors import InvalidCredentialsError
from app.core.errors import ApiError, ErrorCode
from app.main import create_app
from app.modules.auth.schemas import UserPrincipal


@pytest.fixture
def auth_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    from app.api.rest.v1.endpoints import auth as auth_endpoint
    from app.db.session import get_db_session

    async def fake_get_db_session() -> AsyncGenerator[object, None]:
        yield object()

    async def fake_authenticate_user(*_args: object, **_kwargs: object) -> UserPrincipal:
        return UserPrincipal(user_id="user-1", email="user@example.com")

    monkeypatch.setattr(auth_endpoint, "authenticate_user", fake_authenticate_user)

    app = create_app()
    app.dependency_overrides[get_db_session] = fake_get_db_session

    with TestClient(app) as client:
        yield client


def test_login_contract_returns_token_shape(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "12345678"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["access_token"], str)
    assert payload["access_token"]
    assert payload["token_type"] == "bearer"


def test_login_invalid_credentials_uses_error_contract(
    auth_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.api.rest.v1.endpoints import auth as auth_endpoint

    async def fake_authenticate_invalid(*_args: object, **_kwargs: object) -> UserPrincipal:
        raise ApiError(
            code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Invalid credentials",
            status_code=401,
        )

    monkeypatch.setattr(auth_endpoint, "authenticate_user", fake_authenticate_invalid)

    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "bad-pass-1"},
    )

    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTH_INVALID_CREDENTIALS"
    assert "message" in payload["error"]
    assert isinstance(payload["error"]["details"], dict)
    assert "trace_id" in payload["error"]
    assert "X-Trace-Id" in response.headers


def test_login_invalid_credentials_domain_error_uses_error_contract(
    auth_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.api.rest.v1.endpoints import auth as auth_endpoint

    async def fake_authenticate_invalid_domain(*_args: object, **_kwargs: object) -> UserPrincipal:
        raise InvalidCredentialsError()

    monkeypatch.setattr(auth_endpoint, "authenticate_user", fake_authenticate_invalid_domain)

    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "bad-pass-1"},
    )

    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTH_INVALID_CREDENTIALS"
    assert payload["error"]["message"] == "Invalid credentials"
