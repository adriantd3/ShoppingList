from fastapi.testclient import TestClient


def test_validation_error_contract(client: TestClient) -> None:
    response = client.post("/api/v1/auth/login", json={"email": "invalid"})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert "trace_id" in payload["error"]
    assert "X-Trace-Id" in response.headers


def test_forbidden_error_contract(client: TestClient) -> None:
    response = client.get("/api/v1/lists/demo/member-check")

    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTH_TOKEN_INVALID"
    assert "trace_id" in payload["error"]
