from fastapi import APIRouter

from app.api.dependencies import DbSession
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import authenticate_user, issue_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: DbSession) -> TokenResponse:
    principal = await authenticate_user(db, payload)
    return issue_access_token(principal)
