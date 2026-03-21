import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        ("GET", "/api/v1/profile", None),
        ("PATCH", "/api/v1/profile", {"display_name": "Name"}),
        ("GET", "/api/v1/profile/notifications", None),
        ("PATCH", "/api/v1/profile/notifications", {"list_change_push_enabled": False}),
        ("POST", "/api/v1/profile/push-tokens", {"platform": "android", "push_token": "x" * 32}),
    ],
)
def test_profile_routes_require_authentication(
    client: TestClient,
    method: str,
    path: str,
    body: dict[str, object] | None,
) -> None:
    response = client.request(method, path, json=body)

    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTH_TOKEN_INVALID"
