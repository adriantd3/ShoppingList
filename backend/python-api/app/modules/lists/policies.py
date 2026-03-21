from fastapi import Depends

from app.api.dependencies import DbSession
from app.core.errors import ApiError, ErrorCode
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.repository import get_membership_role


async def require_list_membership(
    list_id: str,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> UserPrincipal:
    role = await get_membership_role(db, list_id=list_id, user_id=principal.user_id)
    if role is None:
        raise ApiError(
            code=ErrorCode.FORBIDDEN_LIST_ACCESS,
            message="User does not belong to this list",
            status_code=403,
        )
    return principal


async def require_list_owner(
    list_id: str,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> UserPrincipal:
    role = await get_membership_role(db, list_id=list_id, user_id=principal.user_id)
    if role != "owner":
        raise ApiError(
            code=ErrorCode.FORBIDDEN_LIST_ACCESS,
            message="Owner role required",
            status_code=403,
        )
    return principal
