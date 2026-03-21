from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.core.errors import ApiError, ErrorCode
from app.modules.auth.schemas import LoginRequest
from app.modules.auth.service import authenticate_user


@pytest.mark.asyncio
async def test_authenticate_user_returns_503_when_database_unavailable() -> None:
    db = AsyncMock()
    db.execute.side_effect = SQLAlchemyError("connection failed")

    with pytest.raises(ApiError) as exc:
        await authenticate_user(
            db,
            LoginRequest(email="test@gmail.com", password="stringstring"),
        )

    assert exc.value.code == ErrorCode.INTERNAL_ERROR
    assert exc.value.status_code == 503
    assert exc.value.message == "Authentication service temporarily unavailable"
