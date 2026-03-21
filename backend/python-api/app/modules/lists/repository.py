from decimal import Decimal

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ListItem, ListMembership, ShoppingList


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
