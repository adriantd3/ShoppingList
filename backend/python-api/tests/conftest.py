import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-at-least-32-characters-long")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ENABLE_DOCS", "false")

from app.main import create_app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
