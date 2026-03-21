from decimal import Decimal
from typing import cast

from sqlalchemy import Select, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ListItem, ListMembership, ListSnapshot, ShoppingList


async def get_membership_role(db: AsyncSession, list_id: str, user_id: str) -> str | None:
    stmt: Select[tuple[ListMembership]] = (
        select(ListMembership)
        .where(ListMembership.list_id == list_id)
        .where(ListMembership.user_id == user_id)
    )
    result = await db.execute(stmt)
    membership = result.scalar_one_or_none()
    return membership.role if membership else None


async def list_user_lists(db: AsyncSession, user_id: str) -> list[ShoppingList]:
    stmt: Select[tuple[ShoppingList]] = (
        select(ShoppingList)
        .join(ListMembership, ListMembership.list_id == ShoppingList.id)
        .where(ListMembership.user_id == user_id)
        .order_by(ShoppingList.updated_at.desc(), ShoppingList.id.asc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_list_for_member(db: AsyncSession, list_id: str, user_id: str) -> ShoppingList | None:
    stmt: Select[tuple[ShoppingList]] = (
        select(ShoppingList)
        .join(ListMembership, ListMembership.list_id == ShoppingList.id)
        .where(ShoppingList.id == list_id)
        .where(ListMembership.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_list(db: AsyncSession, *, name: str, owner_user_id: str) -> ShoppingList:
    shopping_list = ShoppingList(name=name, owner_user_id=owner_user_id)
    db.add(shopping_list)
    await db.flush()

    owner_membership = ListMembership(
        list_id=shopping_list.id,
        user_id=owner_user_id,
        role="owner",
    )
    db.add(owner_membership)
    await db.commit()
    await db.refresh(shopping_list)
    return shopping_list


async def update_list_name(db: AsyncSession, shopping_list: ShoppingList, name: str) -> ShoppingList:
    shopping_list.name = name
    await db.commit()
    await db.refresh(shopping_list)
    return shopping_list


async def delete_list(db: AsyncSession, shopping_list: ShoppingList) -> None:
    await db.delete(shopping_list)
    await db.commit()


async def get_next_sort_index(db: AsyncSession, list_id: str) -> int:
    stmt = select(func.max(ListItem.sort_index)).where(ListItem.list_id == list_id)
    result = await db.execute(stmt)
    max_sort_index = result.scalar_one_or_none()
    return 0 if max_sort_index is None else int(max_sort_index) + 1


async def list_items(db: AsyncSession, list_id: str) -> list[ListItem]:
    stmt: Select[tuple[ListItem]] = (
        select(ListItem)
        .where(ListItem.list_id == list_id)
        .order_by(ListItem.sort_index.asc(), ListItem.updated_at.asc(), ListItem.id.asc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_item(
    db: AsyncSession,
    *,
    list_id: str,
    actor_user_id: str,
    name: str,
    quantity: Decimal,
    unit: str,
    category: str,
    note: str | None,
    is_purchased: bool,
    sort_index: int,
) -> ListItem:
    item = ListItem(
        list_id=list_id,
        name=name,
        quantity=quantity,
        unit=unit,
        category=category,
        note=note,
        is_purchased=is_purchased,
        sort_index=sort_index,
        updated_by_user_id=actor_user_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_item_for_list(db: AsyncSession, list_id: str, item_id: str) -> ListItem | None:
    stmt: Select[tuple[ListItem]] = (
        select(ListItem)
        .where(ListItem.id == item_id)
        .where(ListItem.list_id == list_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_item(db: AsyncSession, item: ListItem, *, actor_user_id: str, changes: dict[str, object]) -> ListItem:
    for field_name, field_value in changes.items():
        setattr(item, field_name, field_value)
    item.updated_by_user_id = actor_user_id
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, item: ListItem) -> None:
    await db.delete(item)
    await db.commit()


def serialize_items_snapshot(items: list[ListItem]) -> list[dict[str, object]]:
    return [
        {
            "name": item.name,
            "quantity": str(item.quantity),
            "unit": item.unit,
            "category": item.category,
            "note": item.note,
            "is_purchased": item.is_purchased,
            "is_template_item": item.is_template_item,
            "sort_index": item.sort_index,
        }
        for item in items
    ]


async def create_pre_reset_snapshot(
    db: AsyncSession,
    *,
    list_id: str,
    created_by_user_id: str,
    payload: dict,
) -> ListSnapshot:
    snapshot = ListSnapshot(
        list_id=list_id,
        snapshot_type="pre_reset",
        payload=payload,
        created_by_user_id=created_by_user_id,
    )
    db.add(snapshot)
    await db.flush()
    return snapshot


async def reset_items_purchase_flags(db: AsyncSession, *, list_id: str, actor_user_id: str) -> int:
    count_stmt = select(func.count()).select_from(ListItem).where(ListItem.list_id == list_id)
    count_result = await db.execute(count_stmt)
    affected = int(count_result.scalar_one())

    stmt = (
        update(ListItem)
        .where(ListItem.list_id == list_id)
        .values(is_purchased=False, updated_by_user_id=actor_user_id)
    )
    await db.execute(stmt)
    return affected


async def get_latest_pre_reset_snapshot(db: AsyncSession, *, list_id: str) -> ListSnapshot | None:
    stmt: Select[tuple[ListSnapshot]] = (
        select(ListSnapshot)
        .where(ListSnapshot.list_id == list_id)
        .where(ListSnapshot.snapshot_type == "pre_reset")
        .order_by(desc(ListSnapshot.created_at), desc(ListSnapshot.id))
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def replace_list_items_from_snapshot(
    db: AsyncSession,
    *,
    list_id: str,
    actor_user_id: str,
    snapshot_items: list[dict[str, object]],
) -> int:
    await db.execute(delete(ListItem).where(ListItem.list_id == list_id))

    for item in snapshot_items:
        quantity = cast(str, item["quantity"])
        sort_index_raw = item.get("sort_index", 0)
        restored_item = ListItem(
            list_id=list_id,
            name=str(item["name"]),
            quantity=Decimal(quantity),
            unit=str(item["unit"]),
            category=str(item["category"]),
            note=str(item["note"]) if item.get("note") is not None else None,
            is_purchased=bool(item.get("is_purchased", False)),
            is_template_item=bool(item.get("is_template_item", False)),
            sort_index=int(cast(int, sort_index_raw)),
            updated_by_user_id=actor_user_id,
        )
        db.add(restored_item)

    await db.flush()
    return len(snapshot_items)
