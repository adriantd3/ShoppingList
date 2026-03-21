from datetime import UTC, datetime
from hashlib import sha256
from secrets import token_urlsafe

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApiError, ErrorCode
from app.modules.auth.schemas import UserPrincipal
from app.modules.sharing import repository
from app.modules.sharing.schemas import (
    ShareLinkConsumeRequest,
    ShareLinkConsumeResponse,
    ShareLinkIssueRequest,
    ShareLinkIssueResponse,
    ShareLinkResponse,
    calculate_expiration,
)


def hash_share_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def generate_share_token() -> str:
    return token_urlsafe(32)


async def issue_share_link_for_user(
    db: AsyncSession,
    *,
    list_id: str,
    principal: UserPrincipal,
    payload: ShareLinkIssueRequest,
) -> ShareLinkIssueResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.FORBIDDEN_LIST_ACCESS,
            message="User does not belong to this list",
            status_code=403,
        )

    token = generate_share_token()
    token_hash = hash_share_token(token)
    share_link = await repository.create_share_link(
        db,
        list_id=list_id,
        token_hash=token_hash,
        expires_at=calculate_expiration(payload.expires_in_minutes),
        created_by_user_id=principal.user_id,
    )

    return ShareLinkIssueResponse(
        link=ShareLinkResponse.model_validate(share_link),
        token=token,
    )


async def revoke_share_link_for_user(
    db: AsyncSession,
    *,
    list_id: str,
    share_link_id: str,
    principal: UserPrincipal,
) -> ShareLinkResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.FORBIDDEN_LIST_ACCESS,
            message="User does not belong to this list",
            status_code=403,
        )

    share_link = await repository.get_share_link(db, list_id=list_id, share_link_id=share_link_id)
    if share_link is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="Share link not found",
            status_code=404,
        )

    if share_link.revoked_at is None:
        share_link = await repository.revoke_share_link(db, share_link=share_link, actor_user_id=principal.user_id)

    return ShareLinkResponse.model_validate(share_link)


async def expire_share_link_for_user(
    db: AsyncSession,
    *,
    list_id: str,
    share_link_id: str,
    principal: UserPrincipal,
) -> ShareLinkResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.FORBIDDEN_LIST_ACCESS,
            message="User does not belong to this list",
            status_code=403,
        )

    share_link = await repository.get_share_link(db, list_id=list_id, share_link_id=share_link_id)
    if share_link is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="Share link not found",
            status_code=404,
        )

    if share_link.expires_at > datetime.now(UTC):
        share_link = await repository.expire_share_link(db, share_link=share_link)

    return ShareLinkResponse.model_validate(share_link)


async def consume_share_link_for_user(
    db: AsyncSession,
    *,
    principal: UserPrincipal,
    payload: ShareLinkConsumeRequest,
) -> ShareLinkConsumeResponse:
    share_link = await repository.get_share_link_by_hash(db, token_hash=hash_share_token(payload.token))
    if share_link is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="Share link not found",
            status_code=404,
        )

    if share_link.revoked_at is not None:
        raise ApiError(
            code=ErrorCode.SHARE_LINK_REVOKED,
            message="Share link was revoked",
            status_code=409,
        )

    if share_link.expires_at <= datetime.now(UTC):
        raise ApiError(
            code=ErrorCode.SHARE_LINK_EXPIRED,
            message="Share link is expired",
            status_code=409,
        )

    role = await repository.upsert_member_role(db, list_id=share_link.list_id, user_id=principal.user_id)
    return ShareLinkConsumeResponse(list_id=share_link.list_id, membership_role=role)
