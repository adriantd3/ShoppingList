import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.realtime.manager import connection_manager
from app.modules.realtime.repository import create_realtime_event, publish_notify
from app.modules.realtime.schemas import RealtimeEventEnvelope

LIST_EVENTS_CHANNEL = "shoppinglist.realtime.events"


def _to_notify_payload(envelope: RealtimeEventEnvelope) -> str:
    return envelope.model_dump_json()


async def emit_list_event(
    db: AsyncSession,
    *,
    list_id: str,
    actor_user_id: str,
    event_type: str,
    payload: dict,
    idempotency_key: str | None = None,
) -> RealtimeEventEnvelope:
    event = await create_realtime_event(
        db,
        list_id=list_id,
        event_type=event_type,
        payload=payload,
        idempotency_key=idempotency_key,
    )
    envelope = RealtimeEventEnvelope(
        event_id=event.id,
        event_type=event.event_type,
        list_id=event.list_id,
        occurred_at=event.created_at,
        actor_user_id=actor_user_id,
        payload=event.payload,
        version=1,
    )

    await publish_notify(
        db,
        channel=LIST_EVENTS_CHANNEL,
        payload=_to_notify_payload(envelope),
    )
    await connection_manager.broadcast_event(list_id, json.loads(envelope.model_dump_json()))
    return envelope
