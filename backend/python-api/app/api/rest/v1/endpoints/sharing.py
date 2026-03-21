from fastapi import APIRouter, Depends, status

from app.api.dependencies import DbSession
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.sharing.schemas import (
    ShareLinkConsumeRequest,
    ShareLinkConsumeResponse,
    ShareLinkIssueRequest,
    ShareLinkIssueResponse,
    ShareLinkResponse,
)
from app.modules.sharing.service import (
    consume_share_link_for_user,
    expire_share_link_for_user,
    issue_share_link_for_user,
    revoke_share_link_for_user,
)

lists_router = APIRouter(prefix="/lists", tags=["sharing"])
public_router = APIRouter(tags=["sharing"])


@lists_router.post("/{list_id}/share-links", response_model=ShareLinkIssueResponse, status_code=status.HTTP_201_CREATED)
async def issue_share_link(
    list_id: str,
    payload: ShareLinkIssueRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ShareLinkIssueResponse:
    return await issue_share_link_for_user(db, list_id=list_id, principal=principal, payload=payload)


@lists_router.post("/{list_id}/share-links/{share_link_id}/revoke", response_model=ShareLinkResponse)
async def revoke_share_link(
    list_id: str,
    share_link_id: str,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ShareLinkResponse:
    return await revoke_share_link_for_user(db, list_id=list_id, share_link_id=share_link_id, principal=principal)


@lists_router.post("/{list_id}/share-links/{share_link_id}/expire", response_model=ShareLinkResponse)
async def expire_share_link(
    list_id: str,
    share_link_id: str,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ShareLinkResponse:
    return await expire_share_link_for_user(db, list_id=list_id, share_link_id=share_link_id, principal=principal)


@public_router.post("/share-links/consume", response_model=ShareLinkConsumeResponse)
async def consume_share_link(
    payload: ShareLinkConsumeRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ShareLinkConsumeResponse:
    return await consume_share_link_for_user(db, principal=principal, payload=payload)
