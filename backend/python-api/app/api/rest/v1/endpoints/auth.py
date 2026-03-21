from fastapi import APIRouter, Depends

from app.api.dependencies import DbSession
from app.core.rate_limit import auth_rate_limit_dependency
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import authenticate_user, issue_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: DbSession,
    _: None = Depends(auth_rate_limit_dependency()),
) -> TokenResponse:
    principal = await authenticate_user(db, payload)
    return issue_access_token(principal)
