from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApiError, ErrorCode
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists import repository
from app.modules.lists.schemas import (
    ListCreateRequest,
    ListItemCreateRequest,
    ListItemResponse,
    ListItemUpdateRequest,
    ListResponse,
    ListUpdateRequest,
)


async def list_lists_for_user(db: AsyncSession, principal: UserPrincipal) -> list[ListResponse]:
    shopping_lists = await repository.list_user_lists(db, user_id=principal.user_id)
    return [ListResponse.model_validate(item) for item in shopping_lists]


async def create_list_for_user(db: AsyncSession, principal: UserPrincipal, payload: ListCreateRequest) -> ListResponse:
    shopping_list = await repository.create_list(
        db,
        name=payload.name.strip(),
        owner_user_id=principal.user_id,
    )
    return ListResponse.model_validate(shopping_list)


async def get_list_for_user(db: AsyncSession, principal: UserPrincipal, list_id: str) -> ListResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )
    return ListResponse.model_validate(shopping_list)


async def update_list_for_user(
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
    payload: ListUpdateRequest,
) -> ListResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )
    updated = await repository.update_list_name(db, shopping_list, payload.name.strip())
    return ListResponse.model_validate(updated)


async def delete_list_for_user(db: AsyncSession, principal: UserPrincipal, list_id: str) -> None:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )
    await repository.delete_list(db, shopping_list)


async def list_items_for_user(db: AsyncSession, principal: UserPrincipal, list_id: str) -> list[ListItemResponse]:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )
    items = await repository.list_items(db, list_id=list_id)
    return [ListItemResponse.model_validate(item) for item in items]


async def create_item_for_user(
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
    payload: ListItemCreateRequest,
) -> ListItemResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )

    sort_index = payload.sort_index
    if sort_index is None:
        sort_index = await repository.get_next_sort_index(db, list_id)

    item = await repository.create_item(
        db,
        list_id=list_id,
        actor_user_id=principal.user_id,
        name=payload.name.strip(),
        quantity=payload.quantity,
        unit=payload.unit,
        category=payload.category,
        note=payload.note,
        is_purchased=payload.is_purchased,
        sort_index=sort_index,
    )
    return ListItemResponse.model_validate(item)


async def update_item_for_user(
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
    item_id: str,
    payload: ListItemUpdateRequest,
) -> ListItemResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )

    item = await repository.get_item_for_list(db, list_id=list_id, item_id=item_id)
    if item is None:
        raise ApiError(
            code=ErrorCode.ITEM_NOT_FOUND,
            message="Item not found",
            status_code=404,
        )

    changes = payload.model_dump(exclude_unset=True)
    if "name" in changes and isinstance(changes["name"], str):
        changes["name"] = changes["name"].strip()

    updated = await repository.update_item(
        db,
        item,
        actor_user_id=principal.user_id,
        changes=changes,
    )
    return ListItemResponse.model_validate(updated)


async def delete_item_for_user(db: AsyncSession, principal: UserPrincipal, list_id: str, item_id: str) -> None:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )

    item = await repository.get_item_for_list(db, list_id=list_id, item_id=item_id)
    if item is None:
        raise ApiError(
            code=ErrorCode.ITEM_NOT_FOUND,
            message="Item not found",
            status_code=404,
        )

    await repository.delete_item(db, item)
