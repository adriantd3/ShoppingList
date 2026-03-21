from fastapi import APIRouter, Depends

from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.policies import require_list_membership, require_list_owner

router = APIRouter(prefix="/lists", tags=["security"])


@router.get("/{list_id}/member-check")
async def member_check(
    list_id: str,
    principal: UserPrincipal = Depends(require_list_membership),
) -> dict[str, str]:
    return {"list_id": list_id, "user_id": principal.user_id, "access": "member"}


@router.get("/{list_id}/owner-check")
async def owner_check(
    list_id: str,
    principal: UserPrincipal = Depends(require_list_owner),
) -> dict[str, str]:
    return {"list_id": list_id, "user_id": principal.user_id, "access": "owner"}
