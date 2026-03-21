from fastapi import APIRouter, Depends, status

from app.core.rate_limit import share_link_rate_limit_dependency
from app.modules.auth.context import AuthenticatedContextDep
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
    context: AuthenticatedContextDep,
    _rate_limit: None = Depends(share_link_rate_limit_dependency()),
) -> ShareLinkIssueResponse:
    return await issue_share_link_for_user(
        db=context.db,
        principal=context.principal,
        list_id=list_id,
        payload=payload,
    )


@lists_router.post("/{list_id}/share-links/{share_link_id}/revoke", response_model=ShareLinkResponse)
async def revoke_share_link(
    list_id: str,
    share_link_id: str,
    context: AuthenticatedContextDep,
    _rate_limit: None = Depends(share_link_rate_limit_dependency()),
) -> ShareLinkResponse:
    return await revoke_share_link_for_user(
        db=context.db,
        principal=context.principal,
        list_id=list_id,
        share_link_id=share_link_id,
    )


@lists_router.post("/{list_id}/share-links/{share_link_id}/expire", response_model=ShareLinkResponse)
async def expire_share_link(
    list_id: str,
    share_link_id: str,
    context: AuthenticatedContextDep,
    _rate_limit: None = Depends(share_link_rate_limit_dependency()),
) -> ShareLinkResponse:
    return await expire_share_link_for_user(
        db=context.db,
        principal=context.principal,
        list_id=list_id,
        share_link_id=share_link_id,
    )


@public_router.post("/share-links/consume", response_model=ShareLinkConsumeResponse)
async def consume_share_link(
    payload: ShareLinkConsumeRequest,
    context: AuthenticatedContextDep,
    _rate_limit: None = Depends(share_link_rate_limit_dependency()),
) -> ShareLinkConsumeResponse:
    return await consume_share_link_for_user(
        db=context.db,
        principal=context.principal,
        payload=payload,
    )
