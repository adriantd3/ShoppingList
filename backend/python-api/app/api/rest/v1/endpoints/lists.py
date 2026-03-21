from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import DbSession
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists.schemas import (
    ListCreateRequest,
    ListItemCreateRequest,
    ListItemResponse,
    ListItemUpdateRequest,
    ListResponse,
    ListUpdateRequest,
)
from app.modules.lists.service import (
    create_item_for_user,
    create_list_for_user,
    delete_item_for_user,
    delete_list_for_user,
    get_list_for_user,
    list_items_for_user,
    list_lists_for_user,
    update_item_for_user,
    update_list_for_user,
)

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("", response_model=list[ListResponse])
async def get_lists(db: DbSession, principal: UserPrincipal = Depends(get_current_user)) -> list[ListResponse]:
    return await list_lists_for_user(db, principal)


@router.post("", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list(
    payload: ListCreateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListResponse:
    return await create_list_for_user(db, principal, payload)


@router.get("/{list_id}", response_model=ListResponse)
async def get_list(list_id: str, db: DbSession, principal: UserPrincipal = Depends(get_current_user)) -> ListResponse:
    return await get_list_for_user(db, principal, list_id)


@router.patch("/{list_id}", response_model=ListResponse)
async def patch_list(
    list_id: str,
    payload: ListUpdateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListResponse:
    return await update_list_for_user(db, principal, list_id, payload)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list(list_id: str, db: DbSession, principal: UserPrincipal = Depends(get_current_user)) -> Response:
    await delete_list_for_user(db, principal, list_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{list_id}/items", response_model=list[ListItemResponse])
async def get_list_items(
    list_id: str,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> list[ListItemResponse]:
    return await list_items_for_user(db, principal, list_id)


@router.post("/{list_id}/items", response_model=ListItemResponse, status_code=status.HTTP_201_CREATED)
async def create_list_item(
    list_id: str,
    payload: ListItemCreateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListItemResponse:
    return await create_item_for_user(db, principal, list_id, payload)


@router.patch("/{list_id}/items/{item_id}", response_model=ListItemResponse)
async def patch_list_item(
    list_id: str,
    item_id: str,
    payload: ListItemUpdateRequest,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> ListItemResponse:
    return await update_item_for_user(db, principal, list_id, item_id, payload)


@router.delete("/{list_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_list_item(
    list_id: str,
    item_id: str,
    db: DbSession,
    principal: UserPrincipal = Depends(get_current_user),
) -> Response:
    await delete_item_for_user(db, principal, list_id, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)