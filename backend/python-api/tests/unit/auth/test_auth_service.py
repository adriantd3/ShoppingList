from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.core.domain_errors import AuthenticationServiceUnavailableError
from app.modules.auth.schemas import LoginRequest
from app.modules.auth.service import authenticate_user


@pytest.mark.asyncio
async def test_authenticate_user_returns_503_when_database_unavailable() -> None:
    db = AsyncMock()
    db.execute.side_effect = SQLAlchemyError("connection failed")

    with pytest.raises(AuthenticationServiceUnavailableError) as exc:
        await authenticate_user(
            db,
            LoginRequest(email="test@gmail.com", password="stringstring"),
        )

    assert exc.value.code == "AUTH_SERVICE_UNAVAILABLE"
    assert exc.value.message == "Authentication service temporarily unavailable"
