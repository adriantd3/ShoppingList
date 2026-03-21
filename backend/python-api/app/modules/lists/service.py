from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApiError, ErrorCode
from app.modules.auth.schemas import UserPrincipal
from app.modules.lists import repository
from app.modules.lists.schemas import (
    ListCreateRequest,
    ListItemCreateRequest,
    ListItemResponse,
    ListItemUpdateRequest,
    ListResetResponse,
    ListResponse,
    ListRestoreLatestResponse,
    ListUpdateRequest,
)
from app.modules.realtime.events import (
    EVENT_ITEM_CREATED,
    EVENT_ITEM_DELETED,
    EVENT_ITEM_PURCHASED_TOGGLED,
    EVENT_ITEM_UPDATED,
    EVENT_LIST_RESET_PERFORMED,
    EVENT_LIST_RESTORE_PERFORMED,
)
from app.modules.realtime.service import emit_list_event


async def list_lists_for_user(*, db: AsyncSession, principal: UserPrincipal) -> list[ListResponse]:
    shopping_lists = await repository.list_user_lists(db, user_id=principal.user_id)
    return [ListResponse.model_validate(item) for item in shopping_lists]


async def create_list_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    payload: ListCreateRequest,
) -> ListResponse:
    async with db.begin():
        shopping_list = await repository.create_list(
            db,
            name=payload.name.strip(),
            owner_user_id=principal.user_id,
        )
    return ListResponse.model_validate(shopping_list)


async def get_list_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
) -> ListResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )
    return ListResponse.model_validate(shopping_list)


async def update_list_for_user(
    *,
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
    async with db.begin():
        updated = await repository.update_list_name(db, shopping_list, payload.name.strip())
    return ListResponse.model_validate(updated)


async def delete_list_for_user(*, db: AsyncSession, principal: UserPrincipal, list_id: str) -> None:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )
    async with db.begin():
        await repository.delete_list(db, shopping_list)


async def list_items_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
) -> list[ListItemResponse]:
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
    *,
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

    async with db.begin():
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
    await emit_list_event(
        db,
        list_id=list_id,
        actor_user_id=principal.user_id,
        event_type=EVENT_ITEM_CREATED,
        payload={"item_id": item.id},
    )
    return ListItemResponse.model_validate(item)


async def update_item_for_user(
    *,
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
    previous_is_purchased = item.is_purchased

    async with db.begin():
        updated = await repository.update_item(
            db,
            item,
            actor_user_id=principal.user_id,
            changes=changes,
        )

    event_type = EVENT_ITEM_UPDATED
    if "is_purchased" in changes and previous_is_purchased != updated.is_purchased:
        event_type = EVENT_ITEM_PURCHASED_TOGGLED

    await emit_list_event(
        db,
        list_id=list_id,
        actor_user_id=principal.user_id,
        event_type=event_type,
        payload={"item_id": updated.id, "is_purchased": updated.is_purchased},
    )
    return ListItemResponse.model_validate(updated)


async def delete_item_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
    item_id: str,
) -> None:
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

    deleted_item_id = item.id
    async with db.begin():
        await repository.delete_item(db, item)
    await emit_list_event(
        db,
        list_id=list_id,
        actor_user_id=principal.user_id,
        event_type=EVENT_ITEM_DELETED,
        payload={"item_id": deleted_item_id},
    )


async def reset_list_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
) -> ListResetResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )

    async with db.begin():
        items = await repository.list_items(db, list_id=list_id)
        snapshot_payload = {"items": repository.serialize_items_snapshot(items)}
        snapshot = await repository.create_pre_reset_snapshot(
            db,
            list_id=list_id,
            created_by_user_id=principal.user_id,
            payload=snapshot_payload,
        )
        reset_count = await repository.reset_items_purchase_flags(
            db,
            list_id=list_id,
            actor_user_id=principal.user_id,
        )

    response = ListResetResponse(
        list_id=list_id,
        snapshot_id=snapshot.id,
        reset_items_count=reset_count,
    )
    await emit_list_event(
        db,
        list_id=list_id,
        actor_user_id=principal.user_id,
        event_type=EVENT_LIST_RESET_PERFORMED,
        payload=response.model_dump(),
    )
    return response


async def restore_latest_for_user(
    *,
    db: AsyncSession,
    principal: UserPrincipal,
    list_id: str,
) -> ListRestoreLatestResponse:
    shopping_list = await repository.get_list_for_member(db, list_id=list_id, user_id=principal.user_id)
    if shopping_list is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="List not found",
            status_code=404,
        )

    snapshot = await repository.get_latest_pre_reset_snapshot(db, list_id=list_id)
    if snapshot is None:
        raise ApiError(
            code=ErrorCode.LIST_NOT_FOUND,
            message="No restorable snapshot found",
            status_code=404,
        )

    payload_items = snapshot.payload.get("items", []) if isinstance(snapshot.payload, dict) else []
    snapshot_items = [item for item in payload_items if isinstance(item, dict)]

    async with db.begin():
        restored_count = await repository.replace_list_items_from_snapshot(
            db,
            list_id=list_id,
            actor_user_id=principal.user_id,
            snapshot_items=snapshot_items,
        )

    response = ListRestoreLatestResponse(
        list_id=list_id,
        snapshot_id=snapshot.id,
        restored_items_count=restored_count,
    )
    await emit_list_event(
        db,
        list_id=list_id,
        actor_user_id=principal.user_id,
        event_type=EVENT_LIST_RESTORE_PERFORMED,
        payload=response.model_dump(),
    )
    return response
