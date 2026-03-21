from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.core.rate_limit import rate_limiter
from app.main import create_app
from app.modules.auth.schemas import UserPrincipal


def test_security_headers_are_present(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"


def test_non_json_content_type_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        content="email=user@example.com",
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 415
    assert response.json()["error"]["code"] == "UNSUPPORTED_MEDIA_TYPE"


def test_payload_too_large_is_rejected(client: TestClient) -> None:
    huge_body = "x" * 1100000
    response = client.post(
        "/api/v1/auth/login",
        content=huge_body,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "REQUEST_TOO_LARGE"


def test_auth_login_rate_limit_is_enforced(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.api.rest.v1.endpoints import auth as auth_endpoint

    rate_limiter.reset()
    monkeypatch.setattr(
        auth_endpoint,
        "authenticate_user",
        AsyncMock(return_value=UserPrincipal(user_id="user-1", email="user@example.com")),
    )

    app = create_app()
    with TestClient(app) as test_client:
        responses = [
            test_client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "12345678"})
            for _ in range(11)
        ]

    assert responses[-1].status_code == 429
    assert responses[-1].json()["error"]["code"] == "RATE_LIMIT_EXCEEDED"

    rate_limiter.reset()
