from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RealtimeEvent


async def create_realtime_event(
    db: AsyncSession,
    *,
    list_id: str,
    event_type: str,
    payload: dict,
    idempotency_key: str | None,
) -> RealtimeEvent:
    event = RealtimeEvent(
        list_id=list_id,
        event_type=event_type,
        payload=payload,
        idempotency_key=idempotency_key,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def publish_notify(
    db: AsyncSession,
    *,
    channel: str,
    payload: str,
) -> None:
    bind = db.get_bind()
    if bind is None or bind.dialect.name != "postgresql":
        return

    await db.execute(
        text("SELECT pg_notify(:channel, :payload)"),
        {"channel": channel, "payload": payload},
    )
    await db.commit()
